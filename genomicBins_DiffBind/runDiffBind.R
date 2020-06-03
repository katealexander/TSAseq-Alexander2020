args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("USAGE: runDiffBind.R diffBind_bins_BINSIZE_ BASENAME", call.=FALSE)
} 

library("DiffBind")

prefix <- args[1]
bn <- args[2]

fileNames <- list.files(pattern = paste(prefix, "[1-9].txt", sep=""))

n = 1
for (file in fileNames){
	SON <- dba(sampleSheet=file)
	SON <- dba.count(SON)
	SON <- dba.contrast(SON, categories = DBA_CONDITION, minMembers = 2) 
	SON <- dba.analyze(SON)
	SON.DB <- dba.report(SON, th=1)
	write.table(as.data.frame(SON.DB), sep="\t", file=paste("DiffBindResults_", bn, n, ".txt", sep=""),  quote=FALSE)
	counts <- dba.peakset(SON, bRetrieve = TRUE)
	write.table(as.data.frame(counts), sep="\t", file=paste("counts_", bn, n, ".txt", sep=""), quote=FALSE)
	dba.save(SON, paste(bn, n, ".txt", sep=""))
	n = n + 1
}


