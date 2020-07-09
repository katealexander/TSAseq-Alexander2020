#!/usr/bin/python 


import sys, os, re, numpy as np 

def main(args):
	if not len(args) >= 3: sys.exit("USAGE: python addAverageCountsToPeak.py peakList NtileFiles  > outFile")


	f = open(args[1])
	peaks = {}
	line = f.readline()[:-1]
	while line != "":
		chr = line.split("\t")[0]
		start = int(line.split("\t")[1])
		stop = int(line.split("\t")[2])
		center = (stop-start)/2 + start
		peaks[chr + "\t" + str(start) + "\t" +  str(stop)] = [chr, center, [], [], [], [], [], [] ]
		line = f.readline()[:-1]
	f.close()
	
	for file in args[2:]:
		f = open(file)
		line = f.readline()[:-1]
		header = "chr\tstart\tstop\t" + "\t".join(line.split("\t")[5:])
		line = f.readline()[:-1]
		while line != "":
			items = line.split("\t")
			chr = items[1]
			start = items[2]
			stop = items[3]
			for peak in peaks.keys():
				if peaks[peak][0] == chr and peaks[peak][1] >= int(start) and peaks[peak][1] <= int(stop):
					peaks[peak][2].append(items[6])
					peaks[peak][3].append(items[7])
					peaks[peak][4].append(items[8])
					peaks[peak][5].append(items[9])
					peaks[peak][6].append(items[10])
					peaks[peak][7].append(items[11])

					
			line = f.readline()[:-1]
		f.close()
	
	print header
	
	for peak in peaks.keys():
		averages = []
		for ntile in peaks[peak][2:]:
			average = np.mean(np.asarray(ntile, dtype=np.float32))
			averages.append(average)
      		if str(averages[1]) != 'nan':
			print peak + "\t" + "\t".join(str(i) for i in averages)
		
	
	
if __name__ == "__main__": main(sys.argv)
