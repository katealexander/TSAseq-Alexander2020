## IMR90 p53 targets
p53 targets vary widely between different cell types and conditions. We therefore used our ChIP-seq ([GSE58740](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1418970)) and RNA-seq ([GSE139003](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE139003)) data to generate a list of p53 targets in IMR90 cells. This was a utilitarian approach to understand the consequences of p53-mediated speckle assocaition on gene expression in IMR90 cells, and shouldn't be considered an exhaustive list of p53 targets. Several other [resources](https://p53.iarc.fr/TargetGenes.aspx) are available for annotations of direct p53 targets.

## Functional definition of IMR90 p53 target
We defined a p53 target as a gene within 200kb of a p53 peak in IMR90 cells with p53 activated (treated with Nutlin for 6h) that increased expression (padj < 0.05; DESeq2 analysis) at any point in our Nutlin timecourse RNA-seq data (covering 6h, 9h, and 12h after Nutlin treatment).

## Genes increasing expression in IMR90 cells treated with Nutlin
Overlap of genes (shown using [Venny](https://bioinfogp.cnb.csic.es/tools/venny/)) reveals  that a total of 2766 genes increase after 6h, 9h, or 12h of Nutlin treatment as compared to the DMSO control. 
  
<img src="https://github.com/katealexander/TSAseq-Alexander2020/blob/master/images/Venny.png" alt="drawing" width="500"/>


## Get genes within 200kb of a p53 peak
```
USAGE: python getGenesWithinDistance.py TSS peaks genes distance > outFile
python getGenesWithinDistance.py hg19_TSS.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed  200000 > outFile
```
