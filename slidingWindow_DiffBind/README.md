# Create sliding windows
Usage: python getGenomeBins.py hg19.chrom.sizes binSize
```
python getGenomeBins.py hg19.chrom.sizes 50000
```
This outputs 9 bed files (bins_50000_[1-9].bed) of 50kb windows (binSize), sliding by 5kb (or binSize/10) in each file. 
