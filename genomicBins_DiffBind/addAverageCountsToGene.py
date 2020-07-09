#!/usr/bin/python 
## This script is for 6 samples. If you do not have 6 samples, edit line 24, add additional/subtract lines after/before line 52

import sys, os, re, numpy as np 

def main(args):
	if not len(args) >= 4: sys.exit("USAGE: python addAverageNtileToGene.py geneList TSSs DiffBindCountsFiles  > outFile")


	f = open(args[1])
	geneList = []
	line = f.readline()[:-1]
	while line != "":
		geneList.append(line)
		line = f.readline()[:-1]
	f.close()
	
	genes = {}
	f = open(args[2])
	line = f.readline()[:-1]
	while line != "":
		if line.split("\t")[4] in geneList:
			## add an empty list for every sample in DiffBind analysis, below is for 4 samples
			genes[line.split("\t")[4]] = [line.split("\t")[0], 0, [], [], [], []]
			
			## example for 8 samples:
			#genes[line.split("\t")[4]] = [line.split("\t")[0], 0, [], [], [], [], [] ,[], [], []]
			
			if line.split("\t")[5] == "+":
				genes[line.split("\t")[4]][1] = line.split("\t")[1]
			else:
				genes[line.split("\t")[4]][1] = line.split("\t")[2]
		line = f.readline()[:-1]
	f.close()
	
	for file in args[3:]:
		f = open(file)
		line = f.readline()[:-1]
		header = "Gene\t" + "\t".join(line.split("\t")[5:])
		line = f.readline()[:-1]
		while line != "":
			items = line.split("\t")
			chr = items[1]
			start = items[2]
			stop = items[3]
			for gene in genes.keys():
				if genes[gene][0] == chr and int(genes[gene][1]) >= int(start) and int(genes[gene][1]) <= int(stop):
					genes[gene][2].append(items[6])
					genes[gene][3].append(items[7])
					genes[gene][4].append(items[8])
					genes[gene][5].append(items[9])
					#genes[gene][6].append(items[10])
					#genes[gene][7].append(items[11])
					## add one additional line per sample added in Line 24
					## example for 8 samples:
					# genes[gene][8].append(items[12])
					# genes[gene][9].append(items[13])
					
			line = f.readline()[:-1]
		f.close()
	
	print header
	
	for gene in genes.keys():
		averages = []
		for ntile in genes[gene][2:]:
			average = np.mean(np.asarray(ntile, dtype=np.float32))
			averages.append(average)
      		if str(averages[1]) != 'nan':
			print gene + "\t" + "\t".join(str(i) for i in averages)
		
	
	
if __name__ == "__main__": main(sys.argv)
