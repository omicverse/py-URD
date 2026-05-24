"""End-to-end parity test against pre-computed R reference."""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))
sys.path.insert(0, str(_PORT.parent / "omicverse-rebuildr" / "engine"))
sys.path.insert(0, str(_PORT.parent / "py-destiny"))

import yaml


@pytest.fixture(scope="module")
def parity_outputs():
    manifest = yaml.safe_load((_PORT / "data" / "manifest.yaml").read_text())
    fixture = _PORT / manifest["fixture"]["path"]
    ref_out = _PORT / "data" / "reference_output.json"
    cand_out = _PORT / "data" / "candidate_output.json"

    if not ref_out.exists():
        R_ENV = os.environ.get("R_TEST_ENV", "/scratch/users/steorra/env/CMAP")
        subprocess.run(
            ["conda", "run", "-p", R_ENV, "Rscript",
             str(_PORT / manifest["reference_command"]),
             str(fixture), str(ref_out)],
            check=True, cwd=_PORT, capture_output=True,
        )
    if not cand_out.exists():
        subprocess.run(
            [sys.executable, str(_PORT / manifest["candidate_command"]),
             str(fixture), str(cand_out)],
            check=True, cwd=_PORT, capture_output=True,
        )

    ref = json.loads(ref_out.read_text())
    cand = json.loads(cand_out.read_text())
    return manifest, ref, cand


def _to_array(xs):
    return np.array([np.nan if x is None else float(x) for x in xs])


def test_pseudotime_spearman(parity_outputs):
    manifest, ref, cand = parity_outputs
    from scipy.stats import spearmanr
    pt_r = _to_array(ref["pseudotime"])
    pt_p = _to_array(cand["pseudotime"])
    mask = ~np.isnan(pt_r) & ~np.isnan(pt_p)
    rho = spearmanr(pt_r[mask], pt_p[mask])[0]
    threshold = next(o for o in manifest["outputs"] if o["name"] == "pseudotime")["threshold"]
    print(f"  pseudotime Spearman = {rho:.4f} (threshold {threshold})")
    assert rho >= threshold
