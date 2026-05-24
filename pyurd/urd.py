"""Lightweight URD object — container for diffusion map + flood/walk results.

R has a heavyweight S4 class with ~30 slots; we keep just what the algorithmic
core needs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


@dataclass
class URD:
    """Container.  All matrices index cells by integer position (0-based) or
    cell name (string) consistently across attributes."""

    cell_names: list[str]                            # n cells
    transitions: csr_matrix | None = None            # n × n diffusion transition
    dm_eigenvectors: np.ndarray | None = None        # n × n_eigs
    dm_eigenvalues: np.ndarray | None = None         # n_eigs
    pseudotime: pd.DataFrame = field(default_factory=pd.DataFrame)   # cells × {name}
    walks: dict[str, np.ndarray] = field(default_factory=dict)        # tip → visit-freq vec
    tip_cells: dict[str, list[str]] = field(default_factory=dict)     # tip → list[str]

    @property
    def n_cells(self) -> int:
        return len(self.cell_names)


def createURD(
    data: np.ndarray | pd.DataFrame,
    *,
    cell_names: list[str] | None = None,
) -> URD:
    """Make an empty URD wrapping the given cells.

    Args:
        data: (n_cells × n_features) — used only to get n_cells / cell_names if
              cell_names is None.  Not stored; URD's algorithmic core needs only
              the transition matrix + pseudotime, not the raw expression.
        cell_names: optional explicit list of cell IDs.
    """
    if cell_names is None:
        if isinstance(data, pd.DataFrame):
            cell_names = list(data.index.astype(str))
        else:
            cell_names = [f"cell_{i}" for i in range(np.asarray(data).shape[0])]
    return URD(cell_names=list(cell_names))
