# TSAseq-Alexander2020
The following pipeline was used for differential analysis of SON TSA-seq data upon p53 activation (Alexander 2020). This pipeline supplements available tools for assessing changes in speckle association of chromatin (https://github.com/lgchang27/TSA-Seq-2.0-Analysis; https://github.com/zocean/Norma). It differs from other analysis methods (https://www.biorxiv.org/content/10.1101/824433v1.full; https://doi.org/10.1083/jcb.201807108) in that it utilizes the DiffBind R package to assess changes over multiple window sizes. 

# Requirements
 R packages: DiffBind,
 bedtools (https://bedtools.readthedocs.io/en/latest/content/installation.html)
 Written in Python 2.7

# Input data
