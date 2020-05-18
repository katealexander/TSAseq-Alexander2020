# Genes of interest
In order to run DiffBind on a set of genes of interest (for example p53 targets), genomic intervals are needed. Based on my analysis, 25kb windows centered on the transcription start site have worked well. However, different size windows can be assessed and compared. Be aware that if the genes of interest are too close together, or the window size too large, this could lead to overlapping windows, which will be merged by DiffBind.
## Get intervals of genes centered on the TSS
In this example, the genes of interest are a list of p53 target genes. Here, p53 targets in IMR90 cells, "IMR90_p53targets.txt", is the list of genes that increases upon p53 activation at any time point of an RNA-seq timecourse (Nutlin-treatment for 6h, 9h, or 12h), and are within 200kb of a p53 ChIP-seq peak (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1418970)
```
#USAGE: python getTSS_interval_ofGeneList.py TSSfile geneList interval > outFile
python getTSS_interval_ofGeneList.py hg19_TSS.txt IMR90_p53targets.txt 25000 > IMR90_p53targets_25kbTSSinterval.bed
```
## Run DiffBind

## Extract genes 

## Type I and Type II errors
In addressing the robustness of SON TSA-seq for detecting true positives and true negatives, it is useful to have an independent method of validation, such as immunoDNA-FISH experiments. With this data,
## Cluster profiler for gene ontology
Cluster profiler (https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html) is an R package for statistical analysis and visualization of functional profiles. Breif tutorial: https://guangchuangyu.github.io/2016/01/go-analysis-using-clusterprofiler/
#### In R load gene lists of p53 targets that increase SON signal or do not increase SON signal
```
SONns <- read.table("notIncreasingSON_p53targs.txt", header=F)
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
