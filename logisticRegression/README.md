# Logistic regression
A key question is what features distinguish p53 targets that increase speckle association from those that do not. In my analysis, I found that p53 targets that are near speckles at baseline, in gene dense regions, in the A1 subcompartment, or have more neighboring p53 peaks are more likely to have p53-induced increases in speckle association. To quantify the estimated predictive capacity of each of these variables, I used a logistic regression, applying it to each variable. 
  
In logistic regressions, you can make a model using the combination of several independent variables. In this case, I found that the genome is organized in such a way that HiC subcompartment, gene density, baseline speckle association, and density of p53 peaks are not independent--all four variables are highly correlated with one another. Without additional mechanistic studies, I don't really know which is the key explanitory variable. For this reason, I reported logistic regressions of p53-regulated speckle association for each of the four variables.

## Selection of variables
The variables of interest can be continuous (i.e. SON concentration at baseline) or discrete (i.e. gene dense versus gene sparse). I chose SON concentration at baseline, gene density, HiC subcompartment, and number of neighboring p53 peaks based on my experimental observations. However, additional or other variables can also be examined. Co-linearity should be explored by investigating the relationship between each pair of variables.

## Data used in this analysis
#### p53 peaks
p53 peaks ("GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed") were obtained from a previously published dataset, [GSE58740](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58740).
#### Gene Density
Genomic regions were defined as gene dense or gene sparse based on whether there were greater or fewer than 26 genes/Mb (two standard deviations above the genome-wide mean density) as calculated using a 1Mb sliding window across the genome ("geneDensity.bed"). Gene deserts were also defined, but are not relevant to this analysis.
#### HiC Subcompartments
HiC subcompartments (A1, A2, B1, B2, B3, B4) are calculated based on mapping of chromatin-chromatin pairwise interactions from HiC data. The A compartment interacts more with other A-compartment DNA than with B-compartment DNA. Likewise, the A compartment is segregated into A1 and A2 subcompartments that tend to interact within themselves moreso than with one another. HiC subcompartments were originally designated in 2014 by [Suhas Rao, Erez Lieberman Aiden, and colleagues](https://www.sciencedirect.com/science/article/pii/S0092867414014974). Subsequently, similar compartmentalization has been imputed from HiC data using methods called [SNIPER](https://www.nature.com/articles/s41467-019-12954-4), and [SCI](https://www.nature.com/articles/s41467-020-14974-x). For this analysis, I used HiC subcompartments imputed in IMR90 cells ("IMR90_track_hg19_HiCsubcompartments.bed") downloaded from the article using [SNIPER](https://www.nature.com/articles/s41467-019-12954-4). 
  
Of note, [a study using SON TSA-seq](https://rupress.org/jcb/article/217/11/4025/120670/Mapping-3D-genome-organization-relative-to-nuclear) to map speckle association genome-wide has found that the A1 compartment is highly enriched at the speckle. Thus, it is possible that speckles are the organizing feature for the A1 subcompartment; although additional studies are required to assess causality.
#### SON concentration at baseline
SON concentration at baseline refers to the normalized counts from SON TSA-seq data in the DMSO-treated control. It thus represents a measure of speckle association at baseline, in the absense of p53 activation. This data was extracted from the DiffBindResults file. 

## Setting up the data
Get all of the variables into a table where each row is a gene, and each column is a variable of interest. Speckle association should be 0 for not associated and 1 for associated. Categorical variables should be numbered 1-n. For example, HiC subcompartments are: 1=A1, 2=A2, 3=B1, 4=B2 5=B3.  

This is what I used to get my data formatted into a table:
```
# "USAGE: python getGeneData.py genesAssociated genesNotAssociated TSSs diffBindResultsBins peakFile density HiCsubcompartments > outFile"
python getGeneData.py IMR90_p53targs_upSONpadj0.01.txt IMR90_p53targs_nsSONpadjOver0.1.txt hg19_TSS.txt DiffBindResults_100kb5.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed geneDensity.bed IMR90_track_hg19_HiCsubcompartments.bed > geneData_with100kbBin5_padj0.01.txt
```
"IMR90_p53targs_upSONpadj0.01.txt" and "IMR90_p53targs_nsSONpadjOver0.1.txt" are lists of the IMR90 p53 targets that increase or do not increase speckle association obtained from [sliding window DiffBind analysis of SON TSA-seq data](https://github.com/katealexander/TSAseq-Alexander2020/tree/master/genomicBins_DiffBind)

## Create logistic model in R
I followed instructions from this [tutorial](https://stats.idre.ucla.edu/r/dae/logit-regression/) and this [tutorial](https://stats.idre.ucla.edu/r/dae/logit-regression/)
#### Load data into R
```
b <- read.table("geneData_with100kbBin5_padj0.01.txt", header=T)
head(b)
    gene associated HiC Density numPeaks concDMSO concNutlin
1 PGM2L1          0   1       1        1     9.99       9.50
2 UBE2Q2          0   1       1        2    10.53      10.64
3  RNF11          0   2       1        1     7.17       5.20
4  RNF13          0   2       1        1     7.10       7.77
5    B2M          0   3       1        1     7.93       7.85
6   PRNP          0   1       1        1     9.23       9.70
```
#### Tell R which variables are discrete
```
b$HiC <- as.factor(b$HiC)
b$Density <- as.factor(b$Density)
b$numPeaks <- as.factor(b$numPeaks)
```

### Logistic model
##### Number of p53 peaks logistic regression (discrete variable)
```
mylogit <- glm(associated ~ numPeaks, data = b, family = "binomial")
```
##### Results for number of p53 peaks logistic regression (discrete variable)
```
summary(mylogit)
Call:
glm(formula = associated ~ numPeaks, family = "binomial", data = b)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-0.8873  -0.6899  -0.5480  -0.5480   1.9850  

Coefficients:
            Estimate Std. Error z value Pr(>|z|)    
(Intercept)  -1.8200     0.1083 -16.799  < 2e-16 ***
numPeaks2     0.5058     0.1667   3.034  0.00241 ** 
numPeaks3     1.0909     0.1542   7.073 1.52e-12 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 1486.2  on 1460  degrees of freedom
Residual deviance: 1435.7  on 1458  degrees of freedom
AIC: 1441.7

Number of Fisher Scoring iterations: 4
```

#### Calculating the odds ratio 
The odds ratio is useful for interpreting the degree to which a discrete variable predicts p53-induced speckle association. In this case, the odds ratio is odds of p53-induced speckle association if a gene has two neighboring p53 peaks compared to the odds of speckle association if the gene just has one neighboring p53 peak. Of note, the odds ratio compares only two conditions at once, so we would look at the odds ratio for three peaks versus one peak, or two peaks versus one peak.  
  
The above logistic regression gives us the coefficients of two p53 peaks versus one p53 peak ("numPeaks2"; 0.5058) and of three p53 peaks versus one p53 peak ("numPeaks3"; 1.0909). From here, the odds-ration is e^coefficient (e^0.5058 = 1.66 odds ratio for 2 peaks over 1 peak; e^1.0909 = 3 odds ratio for 3 peaks over 1 peak). 


### Probability prediction
For continuous varaibles, such as the baseline SON concentration ("concDMSO" below), logistic regressions can be visuallized as a graph of prediction probabilities versus the continuous variable. 
```
mylogit <- glm(associated ~ concDMSO, data = b, family = "binomial")
newdata2 <- with(b, data.frame(concDMSO = rep(seq(from = 9, to = 14, length.out = 100), 3)))
newdata3 <- cbind(newdata2, predict(mylogit, newdata = newdata2, type = "link", se = TRUE))
newdata3 <- within(newdata3, {
+ PredictedProb <- plogis(fit)
+ LL <- plogis(fit - (1.96 * se.fit))
+ UL <- plogis(fit + (1.96 * se.fit))
+ })
```
### Plot probability prediction
```
library(ggplot2)
ggplot(newdata3, aes(x = concDMSO, y = PredictedProb)) + geom_ribbon(aes(ymin = LL, ymax = UL), alpha = 0.2) + geom_line(aes(size = 1) + theme_classic()
```
