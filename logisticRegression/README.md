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
python getGeneData.py IMR90_p53targs_upSONpadj0.01.txt IMR90_p53targs_nsSONpadjOver0.1.txt hg19_TSS.txt DiffBindResults_50kb1.txt GSM1418970_p53_Nutlin_Peaks_hg19_FDR1.bed geneDensity.bed IMR90_track_hg19_HiCsubcompartments.bed > geneData_forLogisticRegression.txt
```
"IMR90_p53targs_upSONpadj0.01.txt" and "IMR90_p53targs_nsSONpadjOver0.1.txt" are lists of the IMR90 p53 targets that increase or do not increase speckle association obtained from 

## Create logistic model in R
I followed this tutorial: https://stats.idre.ucla.edu/r/dae/logit-regression/
#### Load data into R
```
b <- read.table("geneData_forLogisticRegression.txt", header=T)
 head(b)
     gene associated HiC Density peaks1to10 peaks10to200 concDMSO concNutlin
1  PGM2L1          0   1       1          1            2     9.99       9.50
2   NAA60          0   1       2          1            2    11.50      11.58
3    FDXR          1   1       2          2            1    10.49      11.44
4    MT1E          0   1       2          1            2    11.16      11.27
5   VDAC2          0   1       1          2            1     9.79       9.70
6 HSBP1L1          0   1       1          1            2     9.44       9.19
```
#### Tell R which variables are discrete
```
b$HiC <- as.factor(b$HiC)
b$Density <- as.factor(b$Density)
b$peaks1to10 <- as.factor(b$peaks1to10)
b$peaks10to200 <- as.factor(b$peaks10to200)
```

### Logistic model
##### All factors
```
mylogit <- glm(associated ~ HiC + Density + peaks1to10 + peaks10to200 + concDMSO, data = b, family = "binomial")
```
##### Results from all factors
```
summary(mylogit)
Call:
glm(formula = associated ~ HiC + Density + peaks1to10 + peaks10to200 + 
    concDMSO, family = "binomial", data = b)

Deviance Residuals: 
     Min        1Q    Median        3Q       Max  
-2.73319  -0.07374  -0.00184   0.00000   2.63938  

Coefficients:
                 Estimate Std. Error z value Pr(>|z|)    
(Intercept)    -3.999e+01  4.074e+00  -9.817   <2e-16 ***
HiC2            1.867e-01  6.434e-01   0.290   0.7716    
HiC3            5.766e-01  7.412e-01   0.778   0.4366    
HiC4            7.663e+00  1.571e+03   0.005   0.9961    
HiC5           -8.243e+00  1.271e+03  -0.006   0.9948    
Density2        8.668e-01  3.399e-01   2.550   0.0108 *  
peaks1to102     7.964e-01  4.162e-01   1.914   0.0557 .  
peaks1to103     1.213e+00  7.072e-01   1.715   0.0864 .  
peaks1to104     2.035e+00  1.136e+01   0.179   0.8578    
peaks1to105     1.901e+01  1.075e+04   0.002   0.9986    
peaks10to2002   5.485e-02  8.266e-01   0.066   0.9471    
peaks10to2003   1.837e-01  8.348e-01   0.220   0.8258    
peaks10to2004  -1.304e-02  8.787e-01  -0.015   0.9882    
peaks10to2005  -1.020e-01  1.009e+00  -0.101   0.9195    
peaks10to2006   1.875e-01  1.129e+00   0.166   0.8681    
peaks10to2007   9.287e-01  1.282e+00   0.724   0.4689    
peaks10to2008  -1.479e+01  4.855e+03  -0.003   0.9976    
peaks10to2009  -2.802e+01  6.439e+03  -0.004   0.9965    
peaks10to20016 -2.608e+00  1.075e+04   0.000   0.9998    
concDMSO        3.380e+00  3.588e-01   9.420   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 914.84  on 1305  degrees of freedom
Residual deviance: 279.67  on 1286  degrees of freedom
AIC: 319.67

Number of Fisher Scoring iterations: 18
```
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
