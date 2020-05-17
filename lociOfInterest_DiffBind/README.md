# Loci of interest
This analysis is for when you have loci of interest for which you would like to compare the characteristics of those that increase speckle association versus those that do not. 
# Genes of interest
In order to run DiffBind on a set of genes of interest (for example p53 targets), genomic intervals are needed. Based on my analysis, 25kb windows centered on the transcription start site have worked well. However, different size windows can be assessed and compared. Be aware that if the genes of interest are too close together, or the window size too large, this could lead to overlapping windows, which will be merged by DiffBind.
## Get intervals of genes centered on the TSS
In this example, "IMR90_p53targets.txt" is the list of genes that increases upon p53 activation at any time point of an RNA-seq timecourse (Nutlin-treatment for 6h, 9h, or 12h), and are within 200kb of a p53 ChIP-seq peak (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1418970)
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

