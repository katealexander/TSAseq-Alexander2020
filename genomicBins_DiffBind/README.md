# DiffBind for SON TSA-seq
The following uses the [DiffBind](https://bioconductor.org/packages/release/bioc/html/DiffBind.html) R package to quantify and assess significance of SON TSA-seq data across genomic windows.

# Create sliding windows
Because the scale of changes observable by SON TSA-seq has yet to be completely explored, I recommend analysis using a range of window sizes, and assessing how the finding match with data from orthologous approaches (i.e. immunoDNA-FISH). The resolution of SON TSA-seq is thought to be ~20kb. In my analysis, I used 25kb, 50kb, 100kb, and 500kb window sizes and compared to DNA-FISH data. Larger window sizes tend to be less noisy comparing replicates and relating to DNA-FISH measured speckle distances, but are also not as sensitive at detecting p53-induced changes in speckle association. 
  
50kb windows (shown below) would be a good starting point for a first run through of the analysis. However, the appropriate bin size may depend on the biological process under investigation.
```
# USAGE: python getGenomeBins.py hg19.chrom.sizes binSize
python getGenomeBins.py hg19.chrom.sizes 50000
```
This outputs 9 bed files (bins_50000_[1-9].bed) of 50kb windows (binSize), sliding by 5kb (or binSize/10) in each file. 

# Make DiffBind sample sheets
To run DiffBind, a sample sheet is needed for each of the 9 bed files of the sliding windows. Start with a template DiffBind sample sheet (example diffBindTemplate.txt), as described by DiffBind [documentation](http://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), leaving out Peaks and PeakCaller columns as in example.

#### Example diffBindTemplate.txt
```
SampleID,Tissue,Factor,Condition,Replicate,bamReads,ControlID,bamControl,Peaks,PeakCaller
SON_CONTROLrep1,IMR90,SON,control,1,SON_control_rep1.bam,INPUT_CONTROL_rep1,INPUT_control_rep1.bam
SON_CONTROLrep2,IMR90,SON,control,2,SON_control_rep2.bam,INPUT_CONTROL_rep2,INPUT_control_rep2.bam
SON_TREATMENTrep1,IMR90,SON,treatment,1,SON_treatment_rep1.bam,INPUT_TREATMENT_rep1,INPUT_treatment_rep1.bam
SON_TREATMENTrep2,IMR90,SON,treatment,2,SON_treatment_rep2.bam,INPUT_TREATMENT_rep2,INPUT_treatment_rep2.bam
```
The Diff Bind template should be named "diffBindTemplate.txt"

#### Generate sample sheets
From diffBindTemplate.txt, create one sample sheet for each sliding window bed file from "create sliding windows"
```
for file in bins_50000_*.bed; do ./runMakeDiffBindFile.sh $file; done
```
This will create 9 DiffBind sample sheets, one for each sliding window, called diffBind_bins_50000_[1-9].txt

#### Example of one of the resulting sample sheets, "diffBind_bins_50000_1.txt"
```
SampleID,Tissue,Factor,Condition,Replicate,bamReads,ControlID,bamControl,Peaks,PeakCaller
SON_CONTROLrep1,IMR90,SON,control,1,SON_control_rep1.bam,INPUT_CONTROL_rep1,INPUT_control_rep1.bam,bins_50000_1.bed,bed
SON_CONTROLrep2,IMR90,SON,control,2,SON_control_rep2.bam,INPUT_CONTROL_rep2,INPUT_control_rep2.bam,bins_50000_1.bed,bed
SON_TREATMENTrep1,IMR90,SON,treatment,1,SON_treatment_rep1.bam,INPUT_TREATMENT_rep1,INPUT_treatment_rep1.bam,bins_50000_1.bed,bed
SON_TREATMENTrep2,IMR90,SON,treatment,2,SON_treatment_rep2.bam,INPUT_TREATMENT_rep2,INPUT_treatment_rep2.bam,bins_50000_1.bed,bed
```
You can also make these manually, if you prefer.

# Run DiffBind
This R script will loop through the 9 DiffBind sample sheets, running DiffBind for each set of bins. It will take a long time to run. 
```
USAGE: Rscript runDiffBind.R diffBind_bins_BINSIZE_ BASENAME
Rscript runDiffBind.R diffBind_bins_50000_ 50kb
```
There will be three output files for each of the 9 bed files.
1. A counts file ("counts_50kb[1-9].txt") containing normalized counts for each sample within each bin.
2. A DiffBind results file ("DiffBindResults_50kb[1-9].txt") containing concentrations for each condition and p-values for the condition
3. The DiffBind object ("dba_50kb[1-9].RData"). This will be highly useful if you would like to utilize any of the other wonderful DiffBind functions on your dataset.

# Extract differential domains and merge
The DiffBind results file generated above includes all bins. Use the following to extract the significant bins (p-value can be altered within script) and concatenate into one BED file. Because SON TSA-seq data is less reliable at higher distances to the speckle (lower SON signals), this script eliminates bins that have SON concentrations below a certain threshold. This threshold can be edited within the script.
#### Extract significant bins
```
## USAGE: python extractNutlinUpSignificant.py diffBindOutput padj > outFile
for file in DiffBindResults_50kb[1-9].txt; do python extractNutlinUpSignificant.py $file 0.01 >> significant_upNutlin_50kb.bed; done

## USAGE: python extractNutlinDownSignificant.py diffBindOutput padj > outFile
for file in DiffBindResults_50kb[1-9].txt; do python extractNutlinDownSignificant.py $file 0.01 >> significant_downNutlin_50kb.bed; done
```
Here, an adjusted p-value (padj) of 0.01 is selected based on trying padj from 0.05 to 1e-5 and comparing to DNA-FISH data from 21 genes that either increased speckle association (7 genes) or did not increase speckle association (14 genes). Based on this, genes that increase SON signal with padj < 0.01 are deemed to increase speckle association, while genes that have padj > 0.1 are deemed to not increase speckle association. 

#### Sort and merge
```
bedtools sort -i significant_upNutlin_50kb.bed > significant_upNutlin_sorted_50kb.bed
bedtools sort -i significant_downNutlin_50kb.bed > significant_downNutlin_sorted_50kb.bed 

bedtools merge -i significant_upNutlin_sorted_50kb.bed > significant_upNutlin_merged_50kb.bed
bedtools merge -i significant_downNutlin_sorted_50kb.bed > significant_downNutlin_merged_50kb.bed
```

# Get list of genes within significant domains
To get a list of genes that fall within significant domains, I used the following Python script.
```
python getGenesWithin.py hg19_TSS.txt significant_upNutlin_merged.bed > significant_upNutlin_merged_genes.txt
```
This gene list can then be compared to expression data to evaluate whether genes that change SON signal are enriched for genes that change expression levels.

