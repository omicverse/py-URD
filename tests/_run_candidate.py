"""Candidate runner — runs pyurd.floodPseudotime on the same Guo fixture."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))
sys.path.insert(0, str(_PORT.parent / "py-destiny"))

import pydestiny
import pyurd


def main():
    fixture_path, output_path = sys.argv[1], sys.argv[2]
    expr = pd.read_csv(fixture_path, index_col=0).to_numpy(dtype=np.float64)
    n = expr.shape[0]
    print(f"[Py] expression: {n} cells x {expr.shape[1]} genes")

    np.random.seed(42)
    dm = pydestiny.DiffusionMap.fit(expr, sigma="local", n_eigs=5, k=20)
    print(f"[Py] DM eigvecs shape: {dm.eigenvectors.shape}")

    cell_names = [f"cell_{i}" for i in range(n)]
    urd = pyurd.URD(cell_names=cell_names, transitions=dm.transitions,
                    dm_eigenvectors=dm.eigenvectors,
                    dm_eigenvalues=dm.eigenvalues)

    floods = pyurd.floodPseudotime(urd, root_cells=list(range(16)), n=50,
                                    minimum_cells_flooded=1, seed=42)
    print(f"[Py] floods shape: {floods.shape}")

    res = pyurd.floodPseudotimeProcess(floods, max_frac_NA=0.9, stability_div=5)
    pt_full = pd.Series(np.nan, index=cell_names)
    pt_full.loc[res["pseudotime"].index] = res["pseudotime"].values
    print(f"[Py] pseudotime: {pt_full.notna().sum()} non-NA of {n}")

    flood_raw = floods.mean(axis=1, skipna=True)
    out = {
        "pseudotime": [None if np.isnan(x) else float(x) for x in pt_full.tolist()],
        "pseudotime_names": cell_names,
        "flood_raw_mean": [None if np.isnan(x) else float(x) for x in flood_raw.reindex(cell_names).tolist()],
        "n_cells": n,
        "n_simulations": 20,
    }
    with open(output_path, "w") as f:
        json.dump(out, f)
    print(f"[Py] wrote {output_path}")


if __name__ == "__main__":
    main()
