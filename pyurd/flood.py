"""Flood-pseudotime — URD's core pseudotime algorithm.

Algorithm (Farrell et al. 2018 supplementary):

1. Normalise the diffusion-map transition matrix so max(row_sum) = 1.
2. For one simulation:
   - Mark `root_cells` as visited at step 0.
   - At each step i, every still-unvisited cell c has flood-probability
        p_c = 1 - Π_{v ∈ visited} (1 - tm[c, v]).
   - Sample Bernoulli(p_c) for each c; cells drawing 1 are marked visited
     and assigned step i.
   - Stop when newly-visited < `minimum_cells_flooded` or all visited.
3. Run `n` simulations and store the step-of-first-visit per cell.

Postprocess:
- For each column j, divide by max(column j) → relative position [0, 1].
- Average across runs → mean pseudotime (final output).
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, issparse

from .urd import URD


def floodBuildTM(urd: URD | None = None, dm_transitions: np.ndarray | csr_matrix | None = None):
    """Normalise transition matrix so max row sum = 1.

    R's `floodBuildTM(object=NULL, dm=NULL)` — pass an URD with `.transitions`
    populated, or a raw transition matrix.
    """
    if urd is not None:
        tm = urd.transitions
    elif dm_transitions is not None:
        tm = dm_transitions
    else:
        raise ValueError("Must provide either urd= or dm_transitions=.")
    if issparse(tm):
        tm = tm.toarray()
    tm = np.asarray(tm, dtype=np.float64)
    row_sums = tm.sum(axis=1)
    tm_norm = tm / row_sums.max()
    return tm_norm


def _combine_probs_row(tm_row_visited: np.ndarray) -> float:
    """Combined visitation probability across visited cells = 1 - Π(1-p)."""
    # Numerically stable via log:
    clipped = np.clip(tm_row_visited, 0.0, 1.0 - 1e-12)
    return 1.0 - np.exp(np.log1p(-clipped).sum())


def floodPseudotimeCalc(
    tm_flood: np.ndarray,
    start_cells: Sequence[int],
    minimum_cells_flooded: int = 2,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """One flood-pseudotime simulation.

    Args:
        tm_flood: (n × n) normalised transition matrix.
        start_cells: indices to initialise as visited (pseudotime 0).
        minimum_cells_flooded: stop when newly visited < this.
        rng: numpy Generator for reproducibility.

    Returns:
        pseudotime (n,) — step-of-first-visit; NaN for cells never flooded.
    """
    if rng is None:
        rng = np.random.default_rng()

    n = tm_flood.shape[0]
    pseudotime = np.full(n, np.nan, dtype=np.float64)

    visited_mask = np.zeros(n, dtype=bool)
    visited_mask[list(start_cells)] = True
    pseudotime[list(start_cells)] = 0.0

    step = 0
    newly_visited_count = minimum_cells_flooded  # priming so the loop runs

    while visited_mask.sum() < n - 1 and newly_visited_count >= minimum_cells_flooded:
        step += 1
        not_visited_idx = np.where(~visited_mask)[0]
        if not_visited_idx.size == 0:
            break

        # Slice tm[not_visited, visited]: probability of visit from each visited cell
        tm_sub = tm_flood[np.ix_(not_visited_idx, np.where(visited_mask)[0])]
        # combine across visited columns:  p = 1 - Π(1-tm[c,v])
        with np.errstate(divide="ignore", invalid="ignore"):
            log_term = np.log1p(-np.clip(tm_sub, 0.0, 1.0 - 1e-12)).sum(axis=1)
            visit_prob = 1.0 - np.exp(log_term)

        # Bernoulli draws
        draws = rng.binomial(1, np.clip(visit_prob, 0.0, 1.0))
        newly_idx = not_visited_idx[draws == 1]
        newly_visited_count = newly_idx.size

        if newly_visited_count > 0:
            visited_mask[newly_idx] = True
            pseudotime[newly_idx] = step

    return pseudotime


def floodPseudotime(
    urd_or_tm,
    root_cells: Sequence[int | str],
    n: int = 20,
    minimum_cells_flooded: int = 2,
    tm_flood: np.ndarray | None = None,
    seed: int | None = None,
) -> pd.DataFrame:
    """Run `n` flood-pseudotime simulations.

    Args:
        urd_or_tm: URD object (will pull `.transitions`), or transition matrix.
        root_cells: starting cell indices OR names (resolved if URD given).
        n: number of simulations to average over.
        minimum_cells_flooded: per-run stopping condition.
        tm_flood: precomputed normalised tm (skips floodBuildTM).
        seed: master RNG seed.

    Returns:
        DataFrame (n_cells × n) — step-of-first-visit per simulation.
        Index = cell names if URD provided, else integer.
    """
    if isinstance(urd_or_tm, URD):
        urd = urd_or_tm
        if tm_flood is None:
            tm_flood = floodBuildTM(urd=urd)
        # resolve cell names → indices
        name_to_idx = {c: i for i, c in enumerate(urd.cell_names)}
        root_idx: list[int] = []
        for r in root_cells:
            if isinstance(r, str):
                root_idx.append(name_to_idx[r])
            else:
                root_idx.append(int(r))
        cell_index = urd.cell_names
    else:
        if tm_flood is None:
            tm_flood = floodBuildTM(dm_transitions=urd_or_tm)
        root_idx = [int(r) for r in root_cells]
        cell_index = list(range(tm_flood.shape[0]))

    n_cells = tm_flood.shape[0]
    parent_rng = np.random.default_rng(seed)

    floods = np.zeros((n_cells, n), dtype=np.float64)
    for j in range(n):
        run_seed = int(parent_rng.integers(0, 2**31))
        rng_j = np.random.default_rng(run_seed)
        floods[:, j] = floodPseudotimeCalc(
            tm_flood, root_idx, minimum_cells_flooded=minimum_cells_flooded, rng=rng_j
        )
    return pd.DataFrame(floods, index=cell_index, columns=[str(i + 1) for i in range(n)])


def floodPseudotimeProcess(
    floods: pd.DataFrame,
    max_frac_NA: float = 0.4,
    stability_div: int = 10,
) -> dict:
    """Aggregate per-run flood matrix into a single pseudotime per cell.

    Each column is rescaled to [0,1] by dividing by its own max, then averaged
    across runs (NaN-aware mean).  Cells with too many NaN draws are dropped.

    Returns:
        dict with:
          pseudotime: pd.Series (final mean across all runs, in [0,1])
          pseudotime_stability: pd.DataFrame (cells × stability_div) — mean at
              progressively larger subsamples, for stability diagnostics
          visit_freq: pd.Series (cells) — number of non-NaN runs at full size
    """
    n_runs = floods.shape[1]
    frac_na = floods.isna().mean(axis=1)
    keep = frac_na <= max_frac_NA
    floods_kept = floods.loc[keep].copy()

    # Rescale each column to [0, 1]
    col_max = floods_kept.max(axis=0, skipna=True).replace(0, np.nan)
    floods_kept = floods_kept.divide(col_max, axis=1)

    # Stability cuts
    cut_sizes = np.ceil(np.linspace(1, n_runs, stability_div)).astype(int)
    stability = pd.DataFrame(
        {
            str(int(k)): floods_kept.iloc[:, :k].mean(axis=1, skipna=True)
            for k in cut_sizes
        },
        index=floods_kept.index,
    )

    visit_freq = floods_kept.notna().sum(axis=1).astype(float)

    pseudotime = stability.iloc[:, -1]
    return {
        "pseudotime": pseudotime,
        "pseudotime_stability": stability,
        "visit_freq": visit_freq,
    }
