#!/usr/bin/env Rscript
# R reference driver — runs URD floodPseudotime + floodPseudotimeProcess on
# the Guo qPCR fixture (computed once via destiny in R).

suppressPackageStartupMessages({
  library(destiny)
  library(URD)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
fixture_path <- args[1]
output_path <- args[2]

# Load (or derive) expression matrix
expr <- as.matrix(read.csv(fixture_path, row.names = 1))
rownames(expr) <- paste0("cell_", seq_len(nrow(expr)))
cat("[R] expression:", dim(expr)[1], "cells x", dim(expr)[2], "genes\n")

set.seed(42)
dm <- destiny::DiffusionMap(expr, sigma = "local", n_eigs = 5, k = 20)
cat("[R] DM eigvecs:", dim(dm@eigenvectors)[1], "x", dim(dm@eigenvectors)[2], "\n")

# Build a minimal URD object — we just need @dm@transitions
# Ensure cell names propagate into the diffusion map transitions matrix
rownames(dm@transitions) <- rownames(expr)
colnames(dm@transitions) <- rownames(expr)
rownames(dm@eigenvectors) <- rownames(expr)

urd <- new("URD")
urd@dm <- dm
urd@diff.data <- as.data.frame(dm@eigenvectors)
rownames(urd@diff.data) <- rownames(expr)
urd@pseudotime <- data.frame(row.names = rownames(expr))

# Flood pseudotime from a cluster of root cells
# (Guo: 1st 16-cell timepoint cells are the developmental root)
root <- rownames(expr)[1:16]
set.seed(42)
floods <- URD::floodPseudotime(urd, root.cells = root, n = 50,
                                minimum.cells.flooded = 1, verbose = FALSE)
cat("[R] floods:", dim(floods)[1], "x", dim(floods)[2], "\n")

urd <- URD::floodPseudotimeProcess(urd, floods, floods.name = "pseudotime",
                                   max.frac.NA = 0.9, stability.div = 5)
pt <- urd@pseudotime$pseudotime
names(pt) <- rownames(urd@pseudotime)
cat("[R] pseudotime: ", sum(!is.na(pt)), "non-NA of ", length(pt), "\n")

out <- list(
  pseudotime = as.numeric(pt),
  pseudotime_names = rownames(urd@pseudotime),
  flood_raw_mean = as.numeric(apply(floods, 1, function(x) mean(x, na.rm = TRUE))),
  n_cells = nrow(expr),
  n_simulations = 20
)
write_json(out, output_path, auto_unbox = TRUE, na = "null", digits = 8)
cat("[R] wrote", output_path, "\n")
