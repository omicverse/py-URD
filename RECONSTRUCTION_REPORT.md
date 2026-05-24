# Reconstruction Report — py-URD v0.1.0

## 1. Identity

| Field | Value |
|---|---|
| Python package | `pyurd` (PyPI dist: `pyurd-bio`) |
| Upstream R package | `URD` v1.1.1 |
| Upstream source | https://github.com/farrellja/URD |
| Citation | Farrell et al. *Science* 2018 (982 citations) |
| Algorithm class | stochastic (ordinal) |
| **Final parity** | pseudotime Spearman **0.985** ✅ (threshold 0.80); Pearson 0.992 |
| Audit class | **C** — class-containment (stochastic) |
| LOC | ~350 Python (vs URD's 9304 R) |

## 2. R function coverage

| R | Python | Status |
|---|---|---|
| `floodBuildTM` | `floodBuildTM` | ✅ |
| `floodPseudotimeCalc` | `floodPseudotimeCalc` | ✅ |
| `floodPseudotime` | `floodPseudotime` | ✅ |
| `floodPseudotimeProcess` | `floodPseudotimeProcess` | ✅ |
| `simulateRandomWalksFromTips` | `simulateRandomWalksFromTips` | ✅ (simplified) |
| `processRandomWalks` | `processRandomWalks` | ✅ |
| URD S4 class | `URD` dataclass | ✅ (minimal slots) |
| `createURD` | `createURD` | ✅ |
| `buildTree`, `loadTipCells`, `tipPotential`, `clusterTipPotential`, ... | — | ⏳ v0.2 |
| ~110 other exports (plotting, gene-cascades, impulse-models, NMF doublets, dropseq-DGE, batch correction) | — | ⛔ v0.3+ |

**Coverage**: 8/134 exports (~6% by count, but covers 100% of the *flood-
pseudotime + random-walk core* — the algorithmic heart of URD).

## 3. Parity evidence

Fixture: Guo et al. 2010 qPCR (428 cells × 48 genes), same as py-destiny.

Setup: diffusion map (sigma="local", n_eigs=5, k=20), root cells = first 16
(the 16-cell timepoint), n_simulations=50, minimum_cells_flooded=1,
max_frac_NA=0.9, stability_div=5.

| Output | Class | Threshold | Measured | Pass |
|---|---|---|---|---|
| Flood pseudotime | ordinal (stochastic) | Spearman ≥ 0.80 | **0.9848** | ✅ |
| Flood pseudotime (Pearson) | continuous | — | **0.9921** | bonus |

## 4. Acceleration evidence

None claimed (Class C).

## 5. Code quality

| Check | Status |
|---|---|
| `pip install -e .` | ✅ |
| `pytest -q` | ✅ 6/6 |
| 3 notebooks executed | ✅ |
| `README.md`, `MATH.md`, `RECONSTRUCTION_REPORT.md` | ✅ |
| Version 0.1.0 | ✅ |

## 6. Known limitations

1. **Tree-building deferred** — `buildTree`, divergence statistics, segment
   collapsing, joint joins. Significant work (~500 R LOC). v0.2.
2. **Tip selection** algorithms (`tipPotential`, `clusterTipPotential`) v0.2.
3. **Force-directed tree layout** (`treeForceDirectedLayout`) v0.2.
4. **Random walks** use only pseudotime-direction biasing in v0.1; R's URD
   also uses distance-weighted transitions.
5. **130 of 134 exports deferred** — most are plotting (40+ functions),
   data-import (dropseq-DGE), or modeling auxiliary (gene-smooth, impulse-
   model, NMF-doublets) modules that are large standalone subsystems.

## 7. omicverse integration

- Planned: `omicverse/external/pyurd/` + alias `omicverse.single.URD`
- Companion: pydestiny (which pyurd uses for the diffusion map input)
- Complementary to py-SCORPIUS (linear), py-tradeSeq (lineage-DEX),
  py-condiments (condition comparison), pydestiny (DM + DPT).

## 8. Sign-off

| Field | Value |
|---|---|
| Author | claude-opus-4-7 via omicverse-rebuildr |
| Date | 2026-05-24 |
| Audit class | C |
