 # Cluster profiler for gene ontology
Cluster profiler (https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html) is an R package for statistical analysis and visualization of functional profiles. Brief tutorial: https://guangchuangyu.github.io/2016/01/go-analysis-using-clusterprofiler/

#### In R, load gene lists of p53 targets that increase SON signal or do not increase SON signal
```
SONns <- read.table("IMR90_p53targs_nsSONpadjOver0.1.txt", header=F)
SONs <- read.table("increasingSON_p53targs.txt", header=F)
row.names(SONns) <- SONns$V1
row.names(SONs) <- SONs$V1
SONnsGene <- row.names(SONns)
SONsGene <- row.names(SONs)
```
#### load libraries
```
library(clusterProfiler)
library(org.Hs.eg.db)
```
#### convert gene symbol
```
SONnsGene.df <- bitr(SONnsGene, fromType = "SYMBOL", toType = c("ENSEMBL", "ENTREZID"), OrgDb = org.Hs.eg.db)
SONsGene.df <- bitr(SONsGene, fromType = "SYMBOL", toType = c("ENSEMBL", "ENTREZID"), OrgDb = org.Hs.eg.db)
```
#### make list of speckle associated and non speckle associated p53 targets
```
geneList <- list(up=SONsGene.df$ENTREZID, ns=SONnsGene.df$ENTREZID)
```
#### run functional gene ontology analysis (GO)
```
y=compareCluster(geneList, fun = "enrichGO", ont = "BP", OrgDb = org.Hs.eg.db)
```
#### simplify GO terms
This collapses similar GO terms. Cutoff can be adjusted for more or less collapsing. See https://guangchuangyu.github.io/2015/10/use-simplify-to-remove-redundancy-of-enriched-go-terms/
```
 Y <- simplify(y, cutoff=0.7)
```
#### plot GO
```
dotplot(Y, showCategory = 20)
```
#### run functional pathway analysis (KEGG)
```
x=compareCluster(geneList, fun = "enrichKEGG", OrgDb = org.Hs.eg.db)
```
#### plot KEGG
```
dotplot(x, showCategory = 20)
```
