# TSAseq-Alexander2020
This pipeline was used for differential analysis of SON TSA-seq data upon p53 activation. It supplements available tools for assessing changes in speckle association of chromatin ([TSA-seq 2.0](https://github.com/lgchang27/TSA-Seq-2020) and [original](https://github.com/zocean/Norma) from [analysis of several cell lines](https://www.biorxiv.org/content/10.1101/824433v2) or [K562 cells](https://doi.org/10.1083/jcb.201807108)). It differs from these analysis methods in that it utilizes the DiffBind R package to assess changes over multiple window sizes.

This analysis was used in [this](https://doi.org/10.1016/j.molcel.2021.03.006) publication, and validated with ~40 DNA-FISH experiments. Contact [Kate](https://bergerlab.med.upenn.edu/people/katherine-alexander-ph-d/) for questions and access. 

# Requirements
R packages: [DiffBind](https://bioconductor.org/packages/release/bioc/html/DiffBind.html), [clusterProfiler](https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html)  
[bedtools](https://bedtools.readthedocs.io/en/latest/content/installation.html)  
Python 2.7  

# Data preparation
From demultiplexed fastq files, paired-end sequencing data was:  
1. Aligned with [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)  
2. Converted to BAM file format
3. Duplicates removed using [Picard](https://gatk.broadinstitute.org/hc/en-us/articles/360037052812-MarkDuplicates-Picard-)  

BAM files with duplicates removed are the starting point for this repository analysis.
# Analysis
### genomicBins_DiffBind
genomicBins_DiffBind uses Python to split the genome into user-specified bin sizes. It then applies DiffBind to these bins to quantify TSA-seq signal and detect significant differences. Significant bins are extracted using Python, then sorted and merged using Bedtools. Finally, the genes within merged significant bins are extracted using Python.
### IMR90_p53targets
IMR90_p53targets explains how IMR90 p53 targets were defined for the purpose of this analysis, and uses Python to obtain genes within 200kb of a p53 peak.
### logisticRegression
logisticRegression demonstrates how to use glm in R to perform logistic regression for variables that predict changes in speckle association of p53 target genes: gene density, number of p53 binding peaks, HiC subcompartment, and baseline speckle association.
### clusterProfiler
clusterProfiler shows how the R package, clusterProfiler, was used to compare gene ontology (GO) and KEGG pathways of IMR90 p53 targets that do or do not increase speckle association upon p53 activation.

