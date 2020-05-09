#!/usr/bin/python 


import sys, os, re 

def main(args):
	if not len(args) == 3: sys.exit("USAGE: python getGenomeBins.py hg19.chrome.sizes binSize")
	binSize = int(args[2])
	stepSize = binSize/10
	outName = "bins_" + str(binSize) + "_"
	o1 = open(outName + str(1) + ".bed", 'w')
	o2 = open(outName + str(2) + ".bed", 'w')
	o3 = open(outName + str(3) + ".bed", 'w')
	o4 = open(outName + str(4) + ".bed", 'w')
	o5 = open(outName + str(5) + ".bed", 'w')
	o6 = open(outName + str(6) + ".bed", 'w')
	o7 = open(outName + str(7) + ".bed", 'w')
	o8 = open(outName + str(8) + ".bed", 'w')
	o9 = open(outName + str(9) + ".bed", 'w')
	
	f = open(args[1])
	line = f.readline()[:-1]
	while line != "":
		chr = line.split("\t")[0]
		start = 1
		stop = binSize 
		while int(stop + stepSize*(binSize/stepSize - 1)) <= int(line.split("\t")[1]):
			o1.write(chr + "\t" + str(start) + "\t" + str(stop) + "\n")
			o2.write(chr + "\t" + str(start + stepSize) + "\t" + str(stop + stepSize) + "\n")
			o3.write(chr + "\t" + str(start + stepSize*2) + "\t" + str(stop + stepSize*2) + "\n")
			o4.write(chr + "\t" + str(start + stepSize*3) + "\t" + str(stop + stepSize*3) + "\n")
			o5.write(chr + "\t" + str(start + stepSize*4) + "\t" + str(stop + stepSize*4) + "\n")
			o6.write(chr + "\t" + str(start + stepSize*5) + "\t" + str(stop + stepSize*5) + "\n")
			o7.write(chr + "\t" + str(start + stepSize*6) + "\t" + str(stop + stepSize*6) + "\n")
			o8.write(chr + "\t" + str(start + stepSize*7) + "\t" + str(stop + stepSize*7) + "\n")
			o9.write(chr + "\t" + str(start + stepSize*8) + "\t" + str(stop + stepSize*8) + "\n")
			start = start + binSize
			stop = stop + binSize
			
		line = f.readline()[:-1]
		
	o1.close()
	o2.close()
	o3.close()
	o4.close()
	o5.close()
	o6.close()
	o7.close()
	o8.close()
	o9.close()
	f.close()
		
	
	
if __name__ == "__main__": main(sys.argv)
