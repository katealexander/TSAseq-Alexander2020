#!/usr/bin/python 


import sys, os, re 

def main(args):
	if not len(args) == 3: sys.exit("USAGE: python makeDiffBindSheet.py templateFile peakFile > outFile")

	f = open(args[1])
	header = f.readline()[:-1]
	print header 
	line = f.readline()[:-1]
	while line != "":
		print line + "," + args[2] + ",bed"
		line = f.readline()[:-1]
		
	
	
if __name__ == "__main__": main(sys.argv)
