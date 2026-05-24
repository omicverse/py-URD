"""Biased random walks from tip cells — URD's lineage attribution algorithm.

For each tip:
  Start at the tip cell.
  At each step, transition to a neighbour with probability tm[current, :],
  rejecting transitions to cells with higher pseudotime (i.e. walking
  *backwards* in developmental time).
  Halt at a root cell (pseudotime <= root_threshold) or after max_steps.
  Record visit frequency for every cell.

The cell-level visit frequency for each tip is the primary input to URD's
buildTree step.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

from .urd import URD


def simulateRandomWalksFromTips(
    urd: URD,
    pseudotime: pd.Series | np.ndarray,
    tip_cells: dict[str, Sequence[int | str]],
    *,
    n_per_tip: int = 1000,
    max_steps: int = 5000,
    root_threshold: float = 0.05,
    seed: int | None = None,
) -> dict[str, pd.DataFrame]:
    """Biased random walks from each tip backwards through pseudotime.

    Args:
        urd: URD with `.transitions` populated.
        pseudotime: per-cell pseudotime in [0,1].
        tip_cells: mapping tip_name → list of tip cell IDs (or indices).
        n_per_tip: walks per tip.
        max_steps: hard walk-length cap.
        root_threshold: walk halts when reaching a cell with pseudotime
                        below this threshold.
        seed: master RNG.

    Returns:
        dict tip_name → pd.DataFrame of shape (n_cells, n_per_tip) — bool/int
        cell-visit frequency per walk.  For aggregation, see `processRandomWalks`.
    """
    if urd.transitions is None:
        raise ValueError("URD object lacks transition matrix.")
    tm = urd.transitions.toarray() if hasattr(urd.transitions, "toarray") else np.asarray(urd.transitions)
    n_cells = tm.shape[0]
    name_to_idx = {c: i for i, c in enumerate(urd.cell_names)}

    if isinstance(pseudotime, pd.Series):
        pt = pseudotime.reindex(urd.cell_names).to_numpy(dtype=np.float64)
    else:
        pt = np.asarray(pseudotime, dtype=np.float64)
    # Pseudotime may have NaN — clip to 1.0 so walks never enter
    pt_safe = np.where(np.isnan(pt), 1.0, pt)

    parent_rng = np.random.default_rng(seed)

    walks_per_tip: dict[str, pd.DataFrame] = {}
    for tip_name, tip_seeds in tip_cells.items():
        tip_idx = []
        for c in tip_seeds:
            if isinstance(c, str):
                tip_idx.append(name_to_idx[c])
            else:
                tip_idx.append(int(c))
        if not tip_idx:
            continue

        visit = np.zeros((n_cells, n_per_tip), dtype=np.float32)
        run_seed = int(parent_rng.integers(0, 2**31))
        rng = np.random.default_rng(run_seed)

        for w in range(n_per_tip):
            start_pos = int(rng.choice(tip_idx))
            current = start_pos
            visit[current, w] = 1.0
            for step_i in range(max_steps):
                row = tm[current].copy()
                # Block forward jumps: any neighbour with pseudotime > current's
                forward_mask = pt_safe > pt_safe[current]
                row = np.where(forward_mask, 0.0, row)
                row[current] = 0.0  # disallow self-loop
                s = row.sum()
                if s <= 0:
                    break
                row /= s
                # Sample next
                nxt = int(rng.choice(n_cells, p=row))
                current = nxt
                visit[current, w] = 1.0
                if pt_safe[current] <= root_threshold:
                    break

        walks_per_tip[tip_name] = pd.DataFrame(
            visit, index=urd.cell_names, columns=[f"walk_{i}" for i in range(n_per_tip)]
        )
    return walks_per_tip


def processRandomWalks(walks_per_tip: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Collapse per-tip walk visit DataFrames to mean visit frequency per cell.

    Returns:
        DataFrame (cells × tips) — fraction of walks visiting each cell.
    """
    out = {tip: df.mean(axis=1) for tip, df in walks_per_tip.items()}
    return pd.DataFrame(out)
