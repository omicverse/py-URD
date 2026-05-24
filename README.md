# py-URD

A **Python port of [URD](https://github.com/farrellja/URD)** (Farrell et al., *Science* 2018) — branching trajectory inference for single-cell RNA-seq via flood-based pseudotime + biased random walks.

- Pure NumPy / SciPy implementation
- v0.1 ships the core algorithmic pipeline:
  - `floodPseudotime` — probabilistic BFS over the diffusion-map transition graph
  - `floodPseudotimeProcess` — aggregate runs into a per-cell pseudotime
  - `simulateRandomWalksFromTips` — biased random walks for lineage attribution
  - `processRandomWalks` — collapse walks into per-cell visit frequencies
- **Pseudotime parity vs R URD on Guo qPCR data (428 cells)**: **Spearman 0.985, Pearson 0.992** (threshold 0.80).

## Install

```bash
pip install pyurd-bio
```
(module name is `pyurd`; the PyPI distribution name `pyurd` was taken, so this package ships as `pyurd-bio`.)

## Quick-start

```python
import pydestiny, pyurd
# 1. Diffusion map for the transition matrix
dm = pydestiny.DiffusionMap.fit(expression, sigma="local", n_eigs=10)
# 2. URD object wrapping cells + transition matrix
urd = pyurd.URD(cell_names=cell_ids, transitions=dm.transitions,
                dm_eigenvectors=dm.eigenvectors, dm_eigenvalues=dm.eigenvalues)
# 3. Flood pseudotime from a cluster of root cells
floods = pyurd.floodPseudotime(urd, root_cells=root_ids, n=50,
                                minimum_cells_flooded=1, seed=42)
pt    = pyurd.floodPseudotimeProcess(floods, max_frac_NA=0.9)["pseudotime"]
# 4. Biased random walks from tips
walks = pyurd.simulateRandomWalksFromTips(
    urd, pseudotime=pt,
    tip_cells={"lineage_A": [cell_a1, cell_a2], "lineage_B": [cell_b1]},
    n_per_tip=1000, seed=42)
visit_freq = pyurd.processRandomWalks(walks)
```

## Function map

| Python | R | Status |
|---|---|---|
| `floodBuildTM` | `floodBuildTM` | ✅ |
| `floodPseudotimeCalc` | `floodPseudotimeCalc` | ✅ |
| `floodPseudotime` | `floodPseudotime` | ✅ |
| `floodPseudotimeProcess` | `floodPseudotimeProcess` | ✅ |
| `simulateRandomWalksFromTips` | `simulateRandomWalksFromTips` | ✅ (simplified) |
| `processRandomWalks` | `processRandomWalks` | ✅ |
| `URD` / `createURD` | `URD` class (S4) / `createURD` | ✅ (minimal) |
| `buildTree` | `buildTree` | ⏳ v0.2 |
| `loadTipCells` | `loadTipCells` | ⏳ v0.2 |
| `tipPotential` | `tipPotential` | ⏳ v0.2 |
| `treeForceDirectedLayout` | `treeForceDirectedLayout` | ⏳ v0.2 |
| ~110 plotting / S4-method / dropseq-import / NMF-doublets functions | (various) | ⛔ v0.3+ |

## Known limitations (v0.1)

1. **Tree-building deferred** (`buildTree`, `assignCellsToSegments`, divergence statistics) → v0.2.
2. **Tip selection** algorithms (`tipPotential`, `clusterTipPotential`) deferred → v0.2.
3. **Force-directed tree layout** deferred → v0.2.
4. **Random walks** in v0.1 use only the forward/back biasing by pseudotime; R's URD also supports a step-size weighting and a more nuanced cell-distance threshold that we will add in v0.2.
5. **dropseq DGE preprocessing**, **NMF doublets**, **batch correction**, **gene cascades**, **impulse models** — all deferred to v0.3+ (these are large standalone modules in URD that we won't reproduce in Python).

## Citation

> Farrell, J. A. et al. *Single-cell reconstruction of developmental trajectories during zebrafish embryogenesis.* Science 360, eaar3131 (2018).

## License

MIT.
