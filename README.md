# TSAseq-Alexander2020
This pipeline was used for differential analysis of SON TSA-seq data upon p53 activation (Alexander 2020). It supplements available tools for assessing changes in speckle association of chromatin (https://github.com/lgchang27/TSA-Seq-2.0-Analysis; https://github.com/zocean/Norma from https://www.biorxiv.org/content/10.1101/824433v1.full; https://doi.org/10.1083/jcb.201807108). It differs from these analysis methods in that it utilizes the DiffBind R package to assess changes over multiple window sizes and genomic features.

# Requirements
R packages: DiffBind  
bedtools (https://bedtools.readthedocs.io/en/latest/content/installation.html)  
Python 2.7  

# Data preparation
From demultiplexed fastq files, paired-end sequencing data was:  
1. Aligned with Bowtie2 (http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)  
2. Converted to BAM file format ()
3. Duplicates removed using Picard (https://gatk.broadinstitute.org/hc/en-us/articles/360037052812-MarkDuplicates-Picard-)  

BAM files with duplicates removed are the starting point for this repository analysis.
