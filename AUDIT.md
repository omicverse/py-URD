## R function coverage audit

### Coverage summary

| Category | Ported | Total | % |
|---|---|---|---|
| Exported R functions | 7 | 135 | 5.2% |
| Internal helpers (reachable) | 1 | 26 | 3.8% |

_Python package exposes 12 unique names._

### Exported R functions

| R function | Python equivalent | Status |
|---|---|---|
| `NMFDoubletsDefineModules` | `—` | ❌ MISSING |
| `NMFDoubletsDetermineCells` | `—` | ❌ MISSING |
| `NMFDoubletsPlotModuleCombos` | `—` | ❌ MISSING |
| `NMFDoubletsPlotModuleThresholds` | `—` | ❌ MISSING |
| `NMFDoubletsPlotModulesInCell` | `—` | ❌ MISSING |
| `URD` | `—` | ❌ MISSING |
| `aucprTestAlongTree` | `—` | ❌ MISSING |
| `aucprTestByFactor` | `—` | ❌ MISSING |
| `aucprThreshold` | `—` | ❌ MISSING |
| `batchComBat` | `—` | ❌ MISSING |
| `binomTestAlongTree` | `—` | ❌ MISSING |
| `branchpointDetailsPreferenceDist` | `—` | ❌ MISSING |
| `branchpointDetailsVisitDist` | `—` | ❌ MISSING |
| `branchpointDetailsVisitTsne` | `—` | ❌ MISSING |
| `branchpointPreferenceLayout` | `—` | ❌ MISSING |
| `buildTree` | `—` | ❌ MISSING |
| `calcDM` | `—` | ❌ MISSING |
| `calcKNN` | `—` | ❌ MISSING |
| `calcPCA` | `—` | ❌ MISSING |
| `calcTsne` | `—` | ❌ MISSING |
| `cellDistByExpression` | `—` | ❌ MISSING |
| `cellsAlongLineage` | `—` | ❌ MISSING |
| `cellsInCluster` | `—` | ❌ MISSING |
| `clusterCentroids` | `—` | ❌ MISSING |
| `clusterDE` | `—` | ❌ MISSING |
| `clusterTipPotential` | `—` | ❌ MISSING |
| `combineSmoothFit` | `—` | ❌ MISSING |
| `combineTipVisitation` | `—` | ❌ MISSING |
| `corner` | `—` | ❌ MISSING |
| `createURD` | `createURD` | ✅ ported |
| `cropSmoothFit` | `—` | ❌ MISSING |
| `cutstring` | `—` | ❌ MISSING |
| `data.for.plot` | `—` | ❌ MISSING |
| `deTTest` | `—` | ❌ MISSING |
| `defaultURDContinuousColors` | `—` | ❌ MISSING |
| `differentialAUCPR` | `—` | ❌ MISSING |
| `dsCombineDGE` | `—` | ❌ MISSING |
| `dsCutoffPlot` | `—` | ❌ MISSING |
| `dsMetaTrim` | `—` | ❌ MISSING |
| `dsReadDGE` | `—` | ❌ MISSING |
| `dsReadStats` | `—` | ❌ MISSING |
| `edgesFromDM` | `—` | ❌ MISSING |
| `findVariableGenes` | `—` | ❌ MISSING |
| `floodBuildTM` | `floodBuildTM` | ✅ ported |
| `floodPseudotime` | `floodPseudotime` | ✅ ported |
| `floodPseudotimeProcess` | `floodPseudotimeProcess` | ✅ ported |
| `geneCascadeHeatmap` | `—` | ❌ MISSING |
| `geneCascadeImpulsePlots` | `—` | ❌ MISSING |
| `geneCascadeProcess` | `—` | ❌ MISSING |
| `geneSmoothFit` | `—` | ❌ MISSING |
| `geneSmoothReduce` | `—` | ❌ MISSING |
| `getBinaryData` | `—` | ❌ MISSING |
| `getUPXData` | `—` | ❌ MISSING |
| `getZData` | `—` | ❌ MISSING |
| `graphClustering` | `—` | ❌ MISSING |
| `gridArrangeMulti` | `—` | ❌ MISSING |
| `groupFromCells` | `—` | ❌ MISSING |
| `importDM` | `—` | ❌ MISSING |
| `impulseFit` | `—` | ❌ MISSING |
| `is.wholenumber` | `—` | ❌ MISSING |
| `knnOutliers` | `—` | ❌ MISSING |
| `loadTipCells` | `—` | ❌ MISSING |
| `logistic` | `—` | ❌ MISSING |
| `markersAUCPR` | `—` | ❌ MISSING |
| `markersBinom` | `—` | ❌ MISSING |
| `matrixReduce` | `—` | ❌ MISSING |
| `mean.of.logs` | `—` | ❌ MISSING |
| `mean.of.logs.pos` | `—` | ❌ MISSING |
| `mean.pos` | `—` | ❌ MISSING |
| `moduleTestAlongTree` | `—` | ❌ MISSING |
| `nameSegments` | `—` | ❌ MISSING |
| `num.mean` | `—` | ❌ MISSING |
| `pcSDPlot` | `—` | ❌ MISSING |
| `pcTopGenes` | `—` | ❌ MISSING |
| `pcaMarchenkoPastur` | `—` | ❌ MISSING |
| `plotBranchpoint` | `—` | ❌ MISSING |
| `plotDim` | `plotDim` | ✅ ported |
| `plotDim3D` | `—` | ❌ MISSING |
| `plotDim3DStoreView` | `—` | ❌ MISSING |
| `plotDimArray` | `—` | ❌ MISSING |
| `plotDimDiscretized` | `—` | ❌ MISSING |
| `plotDimDual` | `—` | ❌ MISSING |
| `plotDimHighlight` | `—` | ❌ MISSING |
| `plotDists` | `—` | ❌ MISSING |
| `plotDot` | `—` | ❌ MISSING |
| `plotScatter` | `—` | ❌ MISSING |
| `plotSmoothFit` | `—` | ❌ MISSING |
| `plotSmoothFitMultiCascade` | `—` | ❌ MISSING |
| `plotTree` | `—` | ❌ MISSING |
| `plotTreeDiscretized` | `—` | ❌ MISSING |
| `plotTreeDual` | `—` | ❌ MISSING |
| `plotTreeForce` | `—` | ❌ MISSING |
| `plotTreeForce2D` | `—` | ❌ MISSING |
| `plotTreeForceDual` | `—` | ❌ MISSING |
| `plotTreeForceStore3DView` | `—` | ❌ MISSING |
| `plotTreeHighlight` | `—` | ❌ MISSING |
| `plotViolin` | `—` | ❌ MISSING |
| `pmax.abs` | `—` | ❌ MISSING |
| `preference` | `—` | ❌ MISSING |
| `processRandomWalks` | `processRandomWalks` | ✅ ported |
| `processRandomWalksFromTips` | `—` | ❌ MISSING |
| `prop.exp` | `—` | ❌ MISSING |
| `prop.nonexp` | `—` | ❌ MISSING |
| `pseudotimeDetermineLogistic` | `—` | ❌ MISSING |
| `pseudotimeMovingWindow` | `—` | ❌ MISSING |
| `pseudotimePlotStabilityCells` | `—` | ❌ MISSING |
| `pseudotimePlotStabilityOverall` | `—` | ❌ MISSING |
| `pseudotimePlotVisits` | `—` | ❌ MISSING |
| `pseudotimeWeightTransitionMatrix` | `—` | ❌ MISSING |
| `putativeCellsInSegment` | `—` | ❌ MISSING |
| `segChildren` | `—` | ❌ MISSING |
| `segChildrenAll` | `—` | ❌ MISSING |
| `segParent` | `—` | ❌ MISSING |
| `segParentAll` | `—` | ❌ MISSING |
| `segSiblings` | `—` | ❌ MISSING |
| `segTerminal` | `—` | ❌ MISSING |
| `seuratToURD` | `—` | ❌ MISSING |
| `simulateRandomWalk` | `—` | ❌ MISSING |
| `simulateRandomWalksFromTips` | `simulateRandomWalksFromTips` | ✅ ported |
| `sum.of.logs` | `—` | ❌ MISSING |
| `tipPotential` | `—` | ❌ MISSING |
| `translateSegmentNames` | `—` | ❌ MISSING |
| `treeForceDirectedLayout` | `—` | ❌ MISSING |
| `treeForcePositionLabels` | `—` | ❌ MISSING |
| `treeForceRotateCoords` | `—` | ❌ MISSING |
| `treeForceStretchCoords` | `—` | ❌ MISSING |
| `treeForceTranslateCoords` | `—` | ❌ MISSING |
| `treeLayoutCells` | `—` | ❌ MISSING |
| `treeLayoutDendrogram` | `—` | ❌ MISSING |
| `treeLayoutElaborate` | `—` | ❌ MISSING |
| `txCutoffPlot` | `—` | ❌ MISSING |
| `txReadDGE` | `—` | ❌ MISSING |
| `txReadsPerCell` | `—` | ❌ MISSING |
| `urdSubset` | `—` | ❌ MISSING |
| `whichCells` | `—` | ❌ MISSING |

### Internal helpers reachable from exports

| R helper | File | Python equivalent | Status |
|---|---|---|---|
| `allSegmentDivergenceByPseudotime` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `assignCellsToNodes` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `assignCellsToSegments` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `collapseShortSegments` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `divergenceKSVisitation` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `divergencePreferenceDip` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `fdlDensity` | `tree-force-layout.R` | `—` | 🔸 missing-or-inlined |
| `floodPseudotimeCalc` | `flood.R` | `floodPseudotimeCalc` | ✅ ported |
| `impulse.dderiv.double` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.deriv.double` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.deriv.single` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.double` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.fit.double` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.fit.single` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.single` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.start.double` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `impulse.start.single` | `impulse.R` | `—` | 🔸 missing-or-inlined |
| `interpolate.points` | `plot-dim-3D.R` | `—` | 🔸 missing-or-inlined |
| `pseudotimeBreakpointByStretch` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `reformatSegmentJoins` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `removeUnitarySegments` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
| `rotateCoords3d` | `tree-force-layout.R` | `—` | 🔸 missing-or-inlined |
| `sigmoid` | `math.R` | `—` | 🔸 missing-or-inlined |
| `translateCoords3d` | `tree-force-layout.R` | `—` | 🔸 missing-or-inlined |
| `txBarcodesIntegerToChar` | `dropseq-dge.R` | `—` | 🔸 missing-or-inlined |
| `visitDivergenceByPseudotime` | `tree-structure.R` | `—` | 🔸 missing-or-inlined |
