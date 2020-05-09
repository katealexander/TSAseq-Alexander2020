# Create sliding windows
Usage: python getGenomeBins.py hg19.chrom.sizes binSize
```
python getGenomeBins.py hg19.chrom.sizes 50000
```
This outputs 9 bed files (bins_50000_[1-9].bed) of 50kb windows (binSize), sliding by 5kb (or binSize/10) in each file. 

# Make DiffBind sample sheets
Start with a template (example diffBindTemplate.txt), as described by DiffBind documentation (http://bioconductor.org/packages/release/bioc/vignettes/DiffBind/inst/doc/DiffBind.pdf), leaving out Peaks and PeakCaller columns as in example.

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

