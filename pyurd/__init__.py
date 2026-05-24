"""pyurd — pure-Python port of URD (Farrell et al. Science 2018).

Reconstructs branching developmental trajectories from scRNA-seq via:
- diffusion-map based pseudotime ("flood" algorithm)
- biased random walks from tip cells to detect lineage visit-frequencies
- tree-building from divergence statistics

v0.1 covers the core algorithmic API: floodPseudotime, floodPseudotimeProcess,
simulateRandomWalksFromTips, processRandomWalks. Plotting + interactive tree-
navigation deferred to v0.2.
"""

from __future__ import annotations

__version__ = "0.1.0"

from .urd import URD, createURD
from .flood import (
    floodBuildTM,
    floodPseudotime,
    floodPseudotimeCalc,
    floodPseudotimeProcess,
)
from .random_walk import simulateRandomWalksFromTips, processRandomWalks

__all__ = [
    "URD",
    "createURD",
    "floodBuildTM",
    "floodPseudotime",
    "floodPseudotimeCalc",
    "floodPseudotimeProcess",
    "simulateRandomWalksFromTips",
    "processRandomWalks",
    "__version__",
]
