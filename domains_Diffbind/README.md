# Assessing domains
This analysis evaluates TSA-seq changes on a domain level with the purpose of being able to compare the features of domains that do or do not increase signal. 
# Obtain TADs
TADs can be obtained from HiC datasets, and have already been computed for several cell types. This analysis used IMR90 TADs (http://chromosome.sdsc.edu/mouse/hi-c/download.html).
### Ensure TADs do not overlap
If TADs overlap by even 1bp, DiffBind will merge the TADs. This python script will add 1bp to the start of a TAD if it was the same as the stop of the previous TAD.
```
python eliminateTADoverlaps.py IMR90.TAD.total.combined.domain > IMR90.TAD.total.combined.domain_noOverlaps.bed
```
This:
```
chr1	760000	1280000
chr1	1280000	1840000
chr1	1840000	2320000
chr1	2320000	3600000
chr1	3760000	6000000
chr1	6200000	6440000
chr1	6440000	7920000
chr1	7960000	8320000
chr1	8320000	8880000
chr1	8880000	9600000
```
Will be changed to this:
```
chr1	760000	1280000
chr1	1280001	1840000
chr1	1840001	2320000
chr1	2320001	3600000
chr1	3760000	6000000
chr1	6200000	6440000
chr1	6440001	7920000
chr1	7960000	8320000
chr1	8320001	8880000
chr1	8880001	9600000
```
# Obtain SPADs

# Run DiffBind
http://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf
```
#USAGE: Rscript runDiffBind.R diffBindSampleSheet.txt PREFIX
Rscript runDiffBind.R diffBindTemplate_TADs.txt TADs
```

