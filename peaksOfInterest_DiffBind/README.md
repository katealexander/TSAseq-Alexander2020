# Peaks of interest
# Run DiffBind
# Logistic regression
A key question is what are the key features that distinguish between peaks that increase speckle association versus the ones that do not. In my analysis, I found that p53 peaks that are within speckle associated domains (SPADs) at baseline, in gene dense regions, in the A1 subcompartment, or have more neighboring p53 peaks are more likely to have p53-induced increases in speckle association. To answer the question of which of these have the most impact on p53-induced changes in speckle association, I used a logistic regression, applying it to each variable on their own or in combination with one another.  
  
I followed this tutorial: https://stats.idre.ucla.edu/r/dae/logit-regression/
## Selection of variables
The variables of interest can be continuous (i.e. SON concentration at baseline)
## Setting up the data

```
python getPeakData.py diffBindResults_peaks_25kb.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed geneDensity.bed IMR90_track_hg19_HiCsubcompartments.bed > p53PeakData_forLogisticRegression.txt
```
