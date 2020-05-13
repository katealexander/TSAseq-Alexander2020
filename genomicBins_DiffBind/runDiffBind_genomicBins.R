args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("USAGE: runDiffBind.R diffBind_bins_BINSIZE_", call.=FALSE)
} 

library("DiffBind")

prefix <- args[1]

fileNames <- list.files(pattern = paste(prefix, "[1-9].txt", sep=""))

n = 1
for (file in fileNames){
	SON <- dba(sampleSheet=file)
	SON <- dba.count(SON)
	SON <- dba.analyze(SON)
	SON.DB <- dba.report(SON, th=1)
	write.table(as.data.frame(SON.DB), sep="\t", file=paste("DiffBindResults_", prefix, n, ".txt", sep=""),  quote=FALSE)
	counts <- dba.peakset(SON, bRetrieve = TRUE)
	write.table(as.data.frame(counts), sep="\t", file=paste("counts_", prefix, n, ".txt", sep=""), quote=FALSE)
	dba.save(SON, paste(prefix, n, ".txt", sep=""))
	n = n + 1
}


