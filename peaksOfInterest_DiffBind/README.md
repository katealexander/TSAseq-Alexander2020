# Peaks of interest
# Run DiffBind
# Logistic regression
A key question is what are the key features that distinguish between peaks or genes that increase speckle association versus the ones that do not. In my analysis, I found that p53 peaks that are within speckle associated domains (SPADs) at baseline, in gene dense regions, in the A1 subcompartment, or have more neighboring p53 peaks are more likely to have p53-induced increases in speckle association. To answer the question of which of these have the most impact on p53-induced changes in speckle association, I used a logistic regression, applying it to each variable on their own or in combination with one another.
## Selection of variables
The variables of interest can be continuous (i.e. SON concentration at baseline) or discrete (i.e. gene dense versus gene sparse). I chose SON concentration at baseline, gene density, HiC subcompartment, and number of neighboring p53 peaks based on my other experimental observations. However, additional or other variables can also be examined.
## Setting up the data

```
python getPeakData.py diffBindResults_peaks_25kb.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed geneDensity.bed IMR90_track_hg19_HiCsubcompartments.bed > p53PeakData_forLogisticRegression.txt
```
## Create logistic model in R
I followed this tutorial: https://stats.idre.ucla.edu/r/dae/logit-regression/
#### Load data into R
```
b <- read.table("p53PeakData_forLogisticRegression.txt", header=T)
head(b)
    chr    start     stop increasedSON concDMSO concNutlin peaksWithin100kb density HiC
1 chr11  1839557  1864557            1     9.00      10.07                1       2   1
2  chr6 36622284 36662847            1    10.24      11.03                3       1   1
3  chr3 48461652 48486652            1    10.31      10.99                2       2   1
4  chr3 48620730 48648431            1    11.03      11.65                2       2   1
5 chr22 50731955 50756955            1    10.67      11.40                1       2   1
6 chr15 40602055 40648391            1    11.43      11.98                3       2   1
```
#### Tell R which variables are discrete
```
b$peaksWithin100kb <- factor(b$peaksWithin100kb)
b$density <- factor(b$density)
b$HiC <- factor(b$HiC)
```
