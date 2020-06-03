#!/usr/bin/python 
## from DiffBind results of p53 peaks, extracts peaks that increase and peaks that do not significantly change with their corresponding DMSO and Nutlin concentrations from DiffBind
## then adds gene density, HiC subcompartment, # of peaks within 100kb (including peak itself)

import sys, os, re 

def main(args):
	if not len(args) == 8: sys.exit("USAGE: python getGeneData.py genesAssociated genesNotAssociated TSSs diffBindResultsBins peakFile density HiCsubcompartments > outFile")

	header = "gene\tassociated\tHiC\tDensity\tnumPeaks\tconcDMSO\tconcNutlin"
	print header
	
	genes = {}
	f = open(args[1])
	line = f.readline()[:-1]
	while line != "":
		genes[line] = ['',0,1, '','',0,0.000,0.000]
		line = f.readline()[:-1]
	f.close
	
	f = open(args[2])
	line = f.readline()[:-1]
	while line != "":
		genes[line] = ['',0,0, '','',0,0.000,0.000]
		line = f.readline()[:-1]
	f.close
	
	f = open(args[3])
	line = f.readline()[:-1]
	while line != "":
		items = line.split("\t")
		if items[4] in genes.keys():
			chr = items[0]
			if items[5] == "+":
				TSS = int(items[1])
			else:
				TSS = int(items[2])
			if items[4] in genes.keys():
				genes[items[4]][0] = chr
				genes[items[4]][1] = TSS
		line = f.readline()[:-1]
	f.close()
	
	f = open(args[4])
	header = f.readline()[:-1]
	line = f.readline()[:-1]
	while line != "":
		items = line.split("\t")
		chr = items[1]
		start = int(items[2])
		stop = int(items[3])
		for gene in genes.keys():
			if genes[gene][0] == chr and genes[gene][1] >= start and genes[gene][1] <= stop:
				genes[gene][6] = items[7]
				genes[gene][7] = items[8]
		line = f.readline()[:-1]
	f.close
	
	## counts the number of p53 peaks within 0-10 and within 10-200 of TSS
	
	for gene in genes.keys():
		f = open(args[5])
		line = f.readline()[:-1]
		geneChr = genes[gene][0]
		geneTSS = genes[gene][1]
		nPeaks = 0
		while line != "":
			chr = line.split("\t")[0]
			start = int(line.split("\t")[1])
			stop = int(line.split("\t")[2])
			center = (stop-start)/2 + start
			if geneChr == chr and abs(geneTSS - center) <= 200000:
				nPeaks += 1
			line = f.readline()[:-1]
		if nPeaks == 1:
			peakGroup = 1
		elif nPeaks == 2:
			peakGroup = 2
		else:
			peakGroup = 3
		genes[gene][5] = peakGroup
		f.close()
	
#	print "getting density"
	for gene in genes.keys():
		f = open(args[6])
		line = f.readline()[:-1]
		geneChr = genes[gene][0]
		geneTSS = genes[gene][1]
		while line != "":
			chr = line.split("\t")[0]
			start = int(line.split("\t")[1])
			stop = int(line.split("\t")[2])
			if geneChr == chr and geneTSS >= start and geneTSS <= stop:
				if line.split("\t")[3] == "Sparse":
					genes[gene][4] = 1
				if line.split("\t")[3] == "Dense": 
					genes[gene][4] = 2
			line = f.readline()[:-1]
		f.close()

	
#	print "getting subcompartment"
	for gene in genes.keys():
		f = open(args[7])
		geneChr = genes[gene][0]
		geneTSS = genes[gene][1]
		line = f.readline()[:-1]
		line = f.readline()[:-1]
		while line != "":
			chr = line.split("\t")[0]
			start = int(line.split("\t")[1])
			stop = int(line.split("\t")[2])
			if chr == geneChr and start <= geneTSS and stop >= geneTSS:
				subcompartment = line.split("\t")[3]
				if subcompartment == "A1":
					subN = '1'
				elif subcompartment == "A2":
					subN = '2'
				elif subcompartment == "B1":
					subN = '3'
				elif subcompartment == "B2":
					subN = '4'
				elif subcompartment == "B3":
					subN = '5'
				else:
					subN = '6'
				genes[gene][3] = subN
				line = f.readline()[:-1]
				break			
			line = f.readline()[:-1]
		f.close()

	

	for gene in genes.keys():
		if genes[gene][3] != "":
			print gene + "\t" + "\t".join(str(x) for x in genes[gene][2:])

	
if __name__ == "__main__": main(sys.argv)
