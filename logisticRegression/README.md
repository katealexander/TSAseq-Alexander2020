# Logistic regression
A key question is what features distinguish p53 targets that increase speckle association from those that do not. In my analysis, I found that p53 targets that are near speckles at baseline, in gene dense regions, in the A1 subcompartment, or have more neighboring p53 peaks are more likely to have p53-induced increases in speckle association. To quantify the estimated predictive capacity of each of these variables, I used a logistic regression, applying it to each variable. 
  
In logistic regressions, you can make a model using the combination of several independent variables. In this case, I found that the genome is organized in such a way that HiC subcompartment, gene density, baseline speckle association, and density of p53 peaks are not independent--all four variables are highly correlated with one another. Without additional mechanistic studies, I don't really know which is the key explanitory variable. For this reason, I reported logistic regressions of p53-regulated speckle association for each of the four variables.

## Selection of variables
The variables of interest can be continuous (i.e. SON concentration at baseline) or discrete (i.e. gene dense versus gene sparse). I chose SON concentration at baseline, gene density, HiC subcompartment, and number of neighboring p53 peaks based on my experimental observations. However, additional or other variables can also be examined. Co-linearity should be explored by investigating the relationship between each pair of variables.

## Setting up the data
Get all of the variables into a table where each row is a gene, and each column is a variable of interest. Speckle association should be 0 for not associated and 1 for associated. Categorical variables should be numbered 1-n. For example, HiC subcompartments are: 1=A1, 2=A2, 3=B1, 4=B2 5=B3.  

This is what I used to get my data formatted into a table:
```
# "USAGE: python getGeneData.py genesAssociated genesNotAssociated TSSs diffBindResultsBins peakFile density HiCsubcompartments > outFile"

# EXAMPLE
python getGeneData.py IMR90_p53targs_upSONpadj0.01.txt IMR90_p53targs_nsSONpadjOver0.1.txt hg19_TSS.txt DiffBindResults_100kb5.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed geneDensity.bed IMR90_track_hg19_HiCsubcompartments.bed > geneData_with100kbBin5_padj0.01.txt
```
"IMR90_p53targs_upSONpadj0.01.txt" and "IMR90_p53targs_nsSONpadjOver0.1.txt" are lists of the IMR90 p53 targets that increase or do not increase speckle association obtained from 

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
The odds ratio is useful for interpreting the degree to which a discrete variable predicts p53-induced speckle association. In this case, the odds ratio is odds of p53-induced speckle association if a gene has two neighboring p53 peaks compared to the odds of speckle association if the gene just has one neighboring p53 peak. Of note, the odds ratio compares only two conditions at once, so we would look at the odds ratio for three nearby peaks versus one nearby peak, or two peaks versus one peak.  
  
The above logistic regression gives us the coefficients of two p53 peaks versus one p53 peak ("numPeaks2"; 0.5058) and of three p53 peaks versus one p53 peak ("numPeaks3"; 1.0909). 



##### Subset of factors
```
mylogit <- glm(associated ~ peaks1to10 + concDMSO, data = b, family = "binomial")
```
##### Results from subset of factors
```
summary(mylogit)

Call:
glm(formula = associated ~ peaks1to10 + concDMSO, family = "binomial", 
    data = b)

Deviance Residuals: 
     Min        1Q    Median        3Q       Max  
-2.61096  -0.08734  -0.00243   0.00000   2.72567  

Coefficients:
            Estimate Std. Error z value Pr(>|z|)    
(Intercept) -39.6969     3.5794 -11.090   <2e-16 ***
peaks1to102   0.8387     0.3653   2.296   0.0217 *  
peaks1to103   1.0899     0.6727   1.620   0.1052    
peaks1to104  -5.2521     2.3215  -2.262   0.0237 *  
peaks1to105  13.3072   882.7434   0.015   0.9880    
concDMSO      3.4130     0.3122  10.933   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 914.84  on 1305  degrees of freedom
Residual deviance: 297.02  on 1300  degrees of freedom
AIC: 309.02

Number of Fisher Scoring iterations: 13

```

### Probability prediction
```
newdata2 <- with(b, data.frame(concDMSO = rep(seq(from = 9, to = 14, length.out = 100), 3), peaks1to10 = factor(rep(1:3, each = 100))))
newdata3 <- cbind(newdata2, predict(mylogit, newdata = newdata2, type = "link", se = TRUE))
newdata3 <- within(newdata3, {
+ PredictedProb <- plogis(fit)
+ LL <- plogis(fit - (1.96 * se.fit))
+ UL <- plogis(fit + (1.96 * se.fit))
+ })
```
### Plot
```
library(ggplot2)
ggplot(newdata3, aes(x = concDMSO, y = PredictedProb)) + geom_ribbon(aes(ymin = LL, ymax = UL, fill = peaks1to10), alpha = 0.2) + geom_line(aes(colour = peaks1to10), size = 1) + theme_classic()
```
