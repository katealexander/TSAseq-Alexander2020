# Create sliding windows
Usage: python getGenomeBins.py hg19.chrom.sizes binSize
```
python getGenomeBins.py hg19.chrom.sizes 50000
```
This outputs 9 bed files (bins_50000_[1-9].bed) of 50kb windows (binSize), sliding by 5kb (or binSize/10) in each file. 

# Make DiffBind sample sheets
To run DiffBind, a sample sheet is needed for each of the 9 bed files of the sliding windows. Start with a template DiffBind sample sheet (example diffBindTemplate.txt), as described by DiffBind documentation (http://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), leaving out Peaks and PeakCaller columns as in example.

#### Example diffBindTemplate.txt
```
SampleID,Tissue,Factor,Condition,Replicate,bamReads,ControlID,bamControl,Peaks,PeakCaller
SON_CONTROLrep1,IMR90,SON,control,1,SON_control_rep1.bam,INPUT_CONTROL_rep1,INPUT_control_rep1.bam
SON_CONTROLrep2,IMR90,SON,control,2,SON_control_rep2.bam,INPUT_CONTROL_rep2,INPUT_control_rep2.bam
SON_CONTROLrep3,IMR90,SON,control,3,SON_control_rep3.bam,INPUT_CONTROL_rep3,INPUT_control_rep3.bam
SON_TREATMENTrep1,IMR90,SON,treatment,1,SON_treatment_rep1.bam,INPUT_TREATMENT_rep1,INPUT_treatment_rep1.bam
SON_TREATMENTrep2,IMR90,SON,treatment,2,SON_treatment_rep2.bam,INPUT_TREATMENT_rep2,INPUT_treatment_rep2.bam
SON_TREATMENTrep3,IMR90,SON,treatment,3,SON_treatment_rep3.bam,INPUT_TREATMENT_rep3,INPUT_treatment_rep3.bam
```
The Diff Bind template should be named "diffBindTemplate.txt"

#### Generate sample sheets
From diffBindTemplate.txt, create one sample sheet for each sliding window bed file from "create sliding windows"
```
for file in bins_50000_*.bed; do ./runMakeDiffBindFile.sh $file; done
```
This will create 9 DiffBind sample sheets, one for each sliding window, called diffBind_bins_50000_[1-9].txt

# Run DiffBind
This R script will loop through the 9 DiffBind sample sheets, running DiffBind for each set of bins. It will take a long time to run. 
```
Rscript runDiffBind_genomicBins.R diffBind_bins_50000_
```
There will be three output files for each of the 9 bed files.
1. A counts file ("counts_diffBind_bins_50000_[1-9].txt") that contains normalized counts for each sample within each bin.
2. A DiffBind results file ("DiffBindResults_diffBind_bins_50000_[1-9].txt") containing concentrations for each condition and p-values for the condition
3. The DiffBind object ("dba_diffBind_bins_50000_[1-9].RData"). This will be highly useful if you would like to do any of the other wonderful DiffBind functions on your dataset.

# Extract differential domains and merge
The DiffBind results file extracted above includes all bins. Use the following to extract the significant bins (p-value can be altered within script) and concatenate into one BED file. Because SON TSA-seq data is less reliable at higher distances to the speckle (lower SON signals), this script eliminates bins that have SON concentrations below a certain threshold. This threshold can be edited within the script.
#### Extract significant bins
```
for file in DiffBindResults_diffBind_bins_50000_[1-9].txt; do python extractNutlinUpSignificant.py $file >> significant_upNutlin_50kb.bed; done

for file in DiffBindResults_diffBind_bins_50000_[1-9].txt; do python extractNutlinDownSignificant.py $file >> significant_downNutlin_50kb.bed; done
```
#### Sort and merge
```
bedtools sort -i significant_upNutlin_50kb.bed > significant_upNutlin_sorted_50kb.bed
bedtools sort -i significant_downNutlin_50kb.bed > significant_downNutlin_sorted_50kb.bed 

bedtools merge -i significant_upNutlin_sorted_50kb.bed > significant_upNutlin_merged_50kb.bed
bedtools merge -i significant_downNutlin_sorted_50kb.bed > significant_downNutlin_merged_50kb.bed
```
# Get list of genes within significant domains
This gene list can then be compared to expression data to evaluate whether genes that change SON signal are enriched for genes that change expression levels.
```
python getGenesWithin.py hg19_TSS.txt significant_upNutlin_merged.bed > significant_upNutlin_merged_genes.txt
```
