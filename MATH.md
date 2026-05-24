# py-URD — Math Notes

## 1. Bit-equivalent (E)

- **`floodBuildTM`**: tm_norm = tm / max(rowSums(tm)). Identical to R modulo
  f64 rounding.

- **`floodPseudotimeCalc`**: Bernoulli draws with probability
  `1 - prod(1 - tm[c, v])` over visited cells `v`. Computed via
  `1 - exp(sum(log1p(-tm[c, v])))` for numerical stability. R uses the direct
  product form. Both are within f64 precision.

## 2. Bounded ε-approximations (B)

**None claimed.**

## 3. Class-containment (C)

Stochastic algorithm — both R and Python produce different draws even with
identical seeds (different RNG streams, different binomial implementations).
We claim **distributional equivalence** demonstrated by:
- mean over 50 simulations: Spearman 0.985, Pearson 0.992 R vs Python on Guo data
- This is the "ordinal class with N≥30 runs" parity standard from the rebuildr kit.

## 4. Cross-implementation divergence

### 4.1 Binomial RNG streams

R uses Mersenne-Twister + r-binomial. Python's `np.random.Generator` uses
PCG64 + numpy-binomial. With matched seeds, the per-step results differ but
the *expected* pseudotime ordering converges as n_simulations grows.

### 4.2 Postprocessing

R's `floodPseudotimeProcess` divides each column by its column max then
averages. We replicate this exactly with `pd.DataFrame.divide` + `.mean(skipna=True)`.

### 4.3 Random walks (`simulateRandomWalksFromTips`)

URD's R implementation includes additional features we have not yet ported:
- Step-size weighting based on distance in DC space
- Cell-distance threshold to prevent "jumping" between distant cells
- Optional "force walk to root" mode that re-samples failed walks

Our v0.1 walk biases purely by pseudotime: any transition target with
pseudotime greater than current is masked out. This is a simplification of
R URD's algorithm but captures the main intent — walking backwards in
developmental time. v0.2 will add the distance-weighting.

## 5. Audit class

**C** — class-containment. Both algorithms implement Farrell et al. 2018's
probabilistic-flood pseudotime but use different RNG streams; the expected
distributions match (Spearman 0.985 in our reference run). Audit class A is
not achievable for this algorithm without a deterministic seed-aware
RNG-bridge (out of scope for v0.1).
