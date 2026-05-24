#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(destiny)
  library(URD)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = TRUE)
out_dir <- args[1]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

expr <- as.matrix(read.csv(file.path(out_dir, "../../data/fixture_guo_expression.csv"), row.names=1))
rownames(expr) <- paste0("cell_", seq_len(nrow(expr)))

set.seed(42)
dm <- destiny::DiffusionMap(expr, sigma="local", n_eigs=5, k=20)
rownames(dm@transitions) <- rownames(expr); colnames(dm@transitions) <- rownames(expr)
rownames(dm@eigenvectors) <- rownames(expr)

urd <- new("URD"); urd@dm <- dm
urd@diff.data <- as.data.frame(dm@eigenvectors); rownames(urd@diff.data) <- rownames(expr)
urd@pseudotime <- data.frame(row.names=rownames(expr))

root <- rownames(expr)[1:16]
set.seed(42)
floods <- URD::floodPseudotime(urd, root.cells=root, n=50, minimum.cells.flooded=1, verbose=FALSE)
urd <- URD::floodPseudotimeProcess(urd, floods, floods.name="pseudotime", max.frac.NA=0.9, stability.div=5)
pt <- urd@pseudotime$pseudotime

# Save pseudotime + eigenvectors so Py uses identical input
write.csv(dm@eigenvectors, file.path(out_dir, "eigenvectors.csv"), row.names=FALSE)
write.csv(data.frame(pt=pt), file.path(out_dir, "pseudotime.csv"), row.names=FALSE)

# Plot using URD::plotDim — but URD requires tSNE; do plain ggplot like vignette
df <- data.frame(DC1=dm@eigenvectors[,1], DC2=dm@eigenvectors[,2], pseudotime=pt)
p <- ggplot(df, aes(x=DC1, y=DC2, color=pseudotime)) +
  geom_point(size=1) + theme_classic() + scale_color_viridis_c() +
  labs(x="DC1", y="DC2", color="pseudotime")
ggsave(file.path(out_dir, "R_pseudotime.png"), p, width=6, height=4, dpi=100)
cat("R plots done\n")
