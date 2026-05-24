# Discovery — py-URD (scaffold; v0.0 not started)

## 1. Is this package already ported?

`python -m engine.discover_omicverse_deps --check URD` → **No existing omicverse port found.**

## 2. Dependency audit + scope assessment

URD (Farrell et al. *Science* 2018, 982 citations) reconstructs branching developmental trajectories from scRNA-seq:
- Diffusion-pseudotime-based tree inference
- Biased random walk from defined root cells
- Branch detection via "tip selection"
- Force-directed tree visualisation

**Size**: 134 exports (!), **9304 R LOC**. The largest in the trajectory roadmap.

**Why this port is hard**:
- 134 exports — many are interactive/diagnostic (`urdSubset`, `plotTree`, ...).
- Core algorithmic core (`buildTree`, `floodPseudotime`, `simulateRandomWalksFromTips`) is well-defined but interlocks with URD's S4 object model (`URD` class with ~30 slots).
- Heavy reliance on `crayon` console-output formatting in algorithms (cosmetic but pollutes the diff).
- Uses `destiny` for diffusion maps under the hood — port depends on completing py-destiny first OR substituting scanpy's dpt.

**Reusable from omicverse**:
- `omicverse.single._diffusionmap` for diffusion-map backbone (not destiny-exact but workable).
- `scanpy.tl.paga` provides a related branching algorithm; URD's biased random walk is unique.

## 3. Decision

**Substantial port (~3-4 weeks)** — defer to a dedicated session. v0.1 minimum scope:
- Just the core algorithmic API:
  - `createURD(counts, metadata)`
  - `calcDM(URD)` (using py-destiny when available, else scanpy.tl.diffmap)
  - `calcTsne(URD)` (cosmetic; scanpy.tl.tsne)
  - `floodPseudotime(URD, root.cells)`
  - `simulateRandomWalksFromTips(URD, tip.cells)`
  - `buildTree(URD)`
- Drop all 70+ plotting / diagnostic exports for v0.1.

## 4. v0.1 roadmap (for a future session)

1. **Subset to 15-20 algorithmic exports** (drop plotting).
2. Port `floodPseudotime` (biased random walk) — pure NumPy.
3. Port `simulateRandomWalksFromTips` — pure NumPy.
4. Port `buildTree` — graph algorithm on the random-walk visit-frequencies.
5. Match against original Farrell 2018 zebrafish data (small subset).

This is by far the largest port in the trajectory roadmap. Expected effort: ~3 weeks of focused work.
