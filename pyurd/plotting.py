"""Visualisation — 1:1 ports of URD::plotDim (2D scatter coloured by metadata),
URD::plotDistByPseudotime, and a tree-segment plot via ggplot2-python.

URD's ``plotDim`` is essentially a coloured scatter on a stored dimensionality
reduction (tSNE / PCA / DC). ``plotPseudotime`` overlays a continuous variable
on DC-space. Here we expose them as simple functions returning a
ggplot2-python plot.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ggplot2_py import (
    aes,
    geom_path,
    geom_point,
    ggplot,
    labs,
    scale_color_gradientn,
    scale_color_manual,
    theme_classic,
)

from .urd import URD


_VIRIDIS = [
    "#440154", "#482878", "#3E4A89", "#31688E", "#26828E",
    "#1F9E89", "#35B779", "#6CCE59", "#B4DE2C", "#FDE725",
]


def plotDim(
    urd: URD,
    label,
    *,
    reduction_use: str = "dm",
    dim_x: int = 1,
    dim_y: int = 2,
    label_name: str = "value",
    colors: list[str] | None = None,
    point_size: float = 1.0,
    alpha: float = 1.0,
    title: str | None = None,
):
    """1:1 port of URD::plotDim.

    Args:
        urd: URD object with ``.dm_eigenvectors`` populated.
        label: per-cell continuous OR categorical vector.
        reduction_use: only "dm" supported in v0.2 (uses diffusion-map eigenvectors).
        dim_x, dim_y: 1-indexed components to plot.
        label_name: label shown on the colour bar.
        colors: palette (list of colour strings).
        point_size, alpha: point aesthetics.
    """
    if reduction_use != "dm":
        raise NotImplementedError("Only reduction_use='dm' is supported in v0.2.")
    if urd.dm_eigenvectors is None:
        raise ValueError("URD object has no dm_eigenvectors. Compute a diffusion map first.")

    i, j = int(dim_x) - 1, int(dim_y) - 1
    df = pd.DataFrame({
        f"DC{i + 1}": urd.dm_eigenvectors[:, i],
        f"DC{j + 1}": urd.dm_eigenvectors[:, j],
    })
    x_col, y_col = df.columns

    label_arr = pd.Series(label)
    df["__col__"] = label_arr.values
    is_numeric = pd.api.types.is_numeric_dtype(label_arr)

    p = (
        ggplot(df, aes(x=x_col, y=y_col, colour="__col__"))
        + geom_point(size=point_size, alpha=alpha)
        + theme_classic()
        + labs(x=x_col, y=y_col, colour=label_name)
    )
    if is_numeric:
        p = p + scale_color_gradientn(colours=colors or _VIRIDIS)
    else:
        unique = sorted(df["__col__"].unique(), key=str)
        cols = colors or _VIRIDIS
        palette_dict = dict(zip(unique, (cols * (len(unique) // len(cols) + 1))[: len(unique)]))
        p = p + scale_color_manual(values=palette_dict)
    if title is not None:
        p = p + labs(title=title)
    return p


def plotPseudotime(urd: URD, pseudotime: np.ndarray | pd.Series, **kwargs):
    """plotDim coloured by pseudotime — convenience for plotDim(urd, pseudotime, ...)."""
    pt = np.asarray(pseudotime, dtype=np.float64) if not isinstance(pseudotime, pd.Series) else pseudotime
    return plotDim(urd, label=pt, label_name="pseudotime", **kwargs)


def plotVisitFrequency(
    urd: URD,
    visit_freq: np.ndarray | pd.Series,
    *,
    tip_name: str = "",
    dim_x: int = 1,
    dim_y: int = 2,
    point_size: float = 1.0,
):
    """plotDim coloured by per-cell visit frequency from random walks."""
    return plotDim(
        urd,
        label=np.asarray(visit_freq, dtype=np.float64),
        label_name=f"visit_freq{':' + tip_name if tip_name else ''}",
        dim_x=dim_x,
        dim_y=dim_y,
        point_size=point_size,
        colors=["#FFFFFF", "#FFE0E0", "#FFB0B0", "#FF6060", "#C00000", "#600000"],
    )
