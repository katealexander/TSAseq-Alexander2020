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

# Scales of analysis
One key question for analysis of SON TSA-seq is what is the appropriate scale of which to measure biologically meaningful changes. This analysis hence examines changes in SON TSA-seq signal across multiple genomic scales and features.
### Genomic bins
The genome is divided into equal-sized bins and differences in SON TSA-seq signal are examined across a sliding scale of bins. Significant bins are then merged. This approach has the advantage of being agnostic to genomic features, and thus captures differences in signal in an unbiased manner. 
### Domains
Regulated changes in speckle association may occur across genomic features such as domains or compartments. For example, one topologically associated domain (TAD) may increase SON signal, while its neighbor TAD does not change. Likewise, there may be speckle associated domains (SPADs) that globally increase speckle association, while others do not. Thus, we quantify SON signal over TADs and SPADs to compare the features of TADs/SPADs that change speckle association versus those that do not. 
### Loci of interest
For gene sets (i.e. p53 targets) or peak sets of interest (i.e. p53 peaks), assessment of SON TSA-seq differences centered on transcription start sites or peaks may be beneficial. Loci-centric analysis has been particularly informative for contrasting target genes that have regulated speckle association with target genes that do not have regulated speckle association.

# Filtering  
A current unknown with SON TSA-seq is the extent to which changes in chromatin state influences laballing efficiency. For example, if chromatin becomes more accessible, might it artificially increase signal as a consequence of more efficient labelling of open chromatin? To account for potentially confounding effects of changes in chromatin state, regions such as ATAC-seq peaks, transcribed regions, and H3K27ac peaks can be filtered out from BAM files. In the case of p53-induced changes in speckle association, this filtering did not have a substancial impact on the overall results.


