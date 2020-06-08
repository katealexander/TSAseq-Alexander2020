#!/usr/bin/python 


import sys, os, re 

def main(args):
	if not len(args) == 3: sys.exit("USAGE: python extractNutlinDownSignificant.py diffBindOutput padj > outFile")

	padj = float(args[2])
	thresholdConcentration = 2
	
	f = open(args[1])
	header = f.readline()[:-1]
	line = f.readline()[:-1]
	while line != "":
		items = line.split("\t")
		if float(items[11]) <= padj and float(items[9]) >= 0 and float(items[8]) >= thresholdConcentration and float(items[7]) >= thresholdConcentration:
			chr = items[1]
			start = items[2]
			stop = items[3]
			print chr + "\t" + str(start) + "\t" + str(stop)
			
		line = f.readline()
		line.strip()
		
	
	
if __name__ == "__main__": main(sys.argv)
