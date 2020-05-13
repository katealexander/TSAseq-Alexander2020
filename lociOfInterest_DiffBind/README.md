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
This will output two files for each of the 9 bed files. A counts file () that contains the normalized counts for each sample within each bin, and a DiffBind results file () that contains the concentrations and statistics for the control and treatment of each bin. 
## Check the effect of open chromatin
One thing to be wary about with SON TSA-seq is if your experimental perturbation influences chromatin accessibility, it may impact the labelling efficiency, artifactually giving open chromatin more TSA labelling. The good news is that open chromatin peaks are more localized (~100-300bp), whereas changes in speckle associaiton are more broad (20-500kb). Thus, with accessibility data, open chromatin peaks can be filtered out.
#### Filter out open chromatin for each bam file
```
bedtools intersect -v -abam file.bam -b IMR90_ATAC_peaks_merged.bed > file_filtered.bam
```
#### Or for all files
```
for file in *.bam; do bedtools intersect -v -abam $file -b IMR90_ATAC_peaks_merged.bed > ${file//.bam/_filtered.bam}; done
```
With the filtered bam file, re-run DiffBind as above. You will need to make a new "diffBindTemplate.txt" file reflecting the names of the filtered bam files. WARNING: This will overwrite the previously done DiffBind analysis if done in the same directory!
# Extract differential domains and merge
The DiffBind results file extracted above includes all bins. Use the following to extract the significant bins (p-value can be altered within script) and concatenate into one BED file. Because SON TSA-seq data is less reliable at higher distances to the speckle (lower SON signals), this script eliminates bins that have SON concentrations below a certian threshold. This threshold be edited within the script.
#### Extract significant bins
```
for file in SON[1-9]_DiffBindResults_50kb.txt; do python extractNutlinUpSignificant.py $file >> significant_upNutlin_50kb.bed; done

for file in SON[1-9]_DiffBindResults_50kb.txt; do python extractNutlinDownSignificant.py $file >> significant_downNutlin_50kb.bed; done
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
# Get average counts for genes
The following extracts the average counts of all bins that contain the TSS. These python scripts are designed for datasets with 6 samples in DiffBind (3 control and 3 treatment). For more or fewer datasets, these two scripts will need to be edited as indicated within the files.
#### For a list of genes of interest
```
python addAverageCountsToGene.py DNAfishGenes.txt hg19_TSS.txt SON[1-9]_50kbcounts.txt > geneListAverageCounts_50kb.txt
```
#### For all genes in the genome
```
python addAverageCountsToAllGenes.py hg19_TSS.txt SON[1-9]_50kbcounts.txt > allGenesCounts_50kb.txt
```