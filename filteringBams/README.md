# Check the effect of open chromatin or transcription
One thing to be wary about with SON TSA-seq is if your experimental perturbation influences chromatin accessibility, it may impact the labelling efficiency, artifactually giving open chromatin more TSA labelling. The good news is that open chromatin peaks are more localized (~100-300bp), whereas changes in speckle associaiton are more broad (20-500kb). Thus, with accessibility data, open chromatin peaks can be filtered out.
# Input files
All that is needed is a bed file with peaks from ATAC-seq, or any other region that may be confounding, such as transcriptionally engaged RNA Pol II or H3K27ac peaks. Keep in mind that the mechanisms driving speckle association are not well understood, and by filtering out these regions, you may very well be filter out some real signal differences. The limit of resolution of SON TSA-seq is thought to be ~20kb for detecting changes in speckle association, so as long as the areas are smaller than this size, most of the real changes should persist. 
#Filtering
#### Filter out open chromatin for each bam file
```
bedtools intersect -v -abam file.bam -b IMR90_ATAC_peaks_merged.bed > file_filtered.bam
```
#### Or for all files
```
for file in *.bam; do bedtools intersect -v -abam $file -b IMR90_ATAC_peaks_merged.bed > ${file//.bam/_filtered.bam}; done
```
With the filtered bam file, re-run DiffBind as above. You will need to make a new "diffBindTemplate.txt" file reflecting the names of the filtered bam files. WARNING: This will overwrite the previously done DiffBind analysis if done in the same directory!
