#!/usr/bin/python 


import sys, os, re 

def main(args):
	if not len(args) == 3: sys.exit("USAGE: python getGenesWithin.py TSS BED > outFile")

	f = open(args[1])
	TSSs = {}
	line = f.readline()[:-1]
	while line != "":
		items = line.split("\t")
		gene = items[4]
		chr = items[0]
		if items[5] ==  "+":
			TSS = items[1]
		else:
			TSS = items[2]
		TSSs[gene] = [chr, TSS]
		line = f.readline()[:-1]
	f.close()
	
	f = open(args[2])
	line = f.readline()[:-1]
	geneList = []
	while line != "":
		items = line.split("\t")
		chr = items[0]
		start = int(items[1])
		stop = int(items[2])
		for gene in TSSs.keys():
			if chr == TSSs[gene][0] and int(TSSs[gene][1]) > (start - 0000) and int(TSSs[gene][1]) < (stop + 0000):
				if gene not in geneList:
					print gene
					geneList.append(gene)
		line = f.readline()[:-1]
	f.close()
		
	
	
if __name__ == "__main__": main(sys.argv)
