"""Render py-URD plots on Guo fixture."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))
sys.path.insert(0, str(_PORT.parent / "py-destiny"))

import pydestiny
import pyurd
from pyurd.plotting import plotPseudotime
from ggplot2_py import ggsave


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    expr = pd.read_csv(_PORT / "data/fixture_guo_expression.csv", index_col=0).to_numpy(dtype=np.float64)
    cell_names = [f"cell_{i}" for i in range(expr.shape[0])]
    np.random.seed(42)
    dm = pydestiny.DiffusionMap.fit(expr, sigma="local", n_eigs=5, k=20)
    urd = pyurd.URD(cell_names=cell_names, transitions=dm.transitions,
                    dm_eigenvectors=dm.eigenvectors, dm_eigenvalues=dm.eigenvalues)
    floods = pyurd.floodPseudotime(urd, root_cells=list(range(16)), n=50,
                                    minimum_cells_flooded=1, seed=42)
    res = pyurd.floodPseudotimeProcess(floods, max_frac_NA=0.9, stability_div=5)
    pt_full = pd.Series(np.nan, index=cell_names)
    pt_full.loc[res["pseudotime"].index] = res["pseudotime"].values

    p = plotPseudotime(urd, pt_full.values, point_size=1)
    ggsave(str(out_dir / "Py_pseudotime.png"), plot=p, width=6, height=4, dpi=100)
    print("done")


if __name__ == "__main__":
    main()
