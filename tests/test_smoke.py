"""Smoke tests for pyurd."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))
sys.path.insert(0, str(_PORT.parent / "py-destiny"))

import pyurd


def test_import():
    assert pyurd.__version__ == "0.1.0"
    assert hasattr(pyurd, "floodPseudotime")
    assert hasattr(pyurd, "floodPseudotimeProcess")
    assert hasattr(pyurd, "simulateRandomWalksFromTips")


def test_create_urd():
    urd = pyurd.createURD(np.random.RandomState(0).randn(20, 10))
    assert urd.n_cells == 20
    assert len(urd.cell_names) == 20


def test_flood_build_tm():
    import pydestiny
    rng = np.random.RandomState(0)
    expr = rng.randn(30, 5)
    dm = pydestiny.DiffusionMap.fit(expr, sigma="local", n_eigs=3, k=10)
    urd = pyurd.URD(cell_names=[f"c{i}" for i in range(30)], transitions=dm.transitions)
    tm = pyurd.floodBuildTM(urd=urd)
    assert tm.shape == (30, 30)
    assert tm.sum(axis=1).max() <= 1.0 + 1e-9


def test_flood_pseudotime_runs():
    import pydestiny
    rng = np.random.RandomState(0)
    expr = rng.randn(50, 5)
    dm = pydestiny.DiffusionMap.fit(expr, sigma="local", n_eigs=3, k=15)
    urd = pyurd.URD(cell_names=[f"c{i}" for i in range(50)], transitions=dm.transitions)
    floods = pyurd.floodPseudotime(urd, root_cells=[0, 1, 2], n=5,
                                    minimum_cells_flooded=1, seed=0)
    assert floods.shape == (50, 5)


def test_flood_pseudotime_process():
    rng = np.random.RandomState(0)
    floods = pd.DataFrame(rng.randint(0, 20, size=(50, 10)).astype(float),
                          index=[f"c{i}" for i in range(50)])
    res = pyurd.floodPseudotimeProcess(floods, max_frac_NA=0.9, stability_div=3)
    assert "pseudotime" in res
    assert res["pseudotime"].max() <= 1.0
    assert res["pseudotime"].min() >= 0.0
