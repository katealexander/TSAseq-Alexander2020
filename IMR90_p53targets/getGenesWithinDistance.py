#!/usr/bin/python 


import sys, os, re 

def main(args):
	if not len(args) == 5: sys.exit("USAGE: python getGenesWithinDistance.py TSS peaks genes distance > outFile")

	distance = int(args[4])
	
	f = open(args[1])
	TSSs = {}
	line = f.readline()[:-1]
	while line != "":
		items = line.split("\t")
		gene = items[4]
		chr = items[0]
		if items[5] ==  "+":
			TSS = int(items[1])
		else:
			TSS = int(items[2])
		TSSs[gene] = [chr, TSS]
		line = f.readline()[:-1]
	f.close()
	
	f = open(args[2])
	peaks = []
	line = f.readline()[:-1]
	while line != "":
		chr = line.split("\t")[0]
		start = int(line.split("\t")[1])
		stop = int(line.split("\t")[2])
		center = (stop-start)/2 + start
		peaks.append([chr, center])
		line = f.readline()[:-1]
	f.close()
	
	
	f = open(args[3])
	line = f.readline()[:-1]
	while line != "":
		gene = line.split("\t")[0]
		if gene not in TSSs.keys():
			line = f.readline()[:-1]
			continue
		dist = 1000000000
		distCurr = 1000000000
		for peak in peaks:
			if peak[0] == TSSs[gene][0]:
				distCurr = abs(peak[1] - TSSs[gene][1])
			if distCurr < dist:
				dist = distCurr
		if dist < distance:
			print gene
			
		line = f.readline()[:-1]
	f.close()	

	

	
if __name__ == "__main__": main(sys.argv)
