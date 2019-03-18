library(dplyr)
library(jsonlite)


args <- commandArgs(TRUE)
filename <- args[1]

x <- read.csv(filename, header=F, stringsAsFactors=F)
result <- data.frame(a="hello", b="world", c="neat")
i <- 2
initnode <- x[1,2]
rowcount <- nrow(x)
firstrow <- x[1,c(2,7)]
names(firstrow) <- c('a', 'b')
datapoints <- list(pml=x[1,3], energia= x[1,4], perdidas= x[1,5], congestion= x[1,6])
while(i <= rowcount) {
	# cat(paste(initnode, x[i,2], "\n", sep="\t"))
	while(i <= rowcount & x[i,2] == initnode) {
		datapoints$pml <- c(datapoints$pml, x[i,3])
		datapoints$energia <- c(datapoints$energia, x[i,4])
		datapoints$perdidas <- c(datapoints$perdidas, x[i,5])
		datapoints$congestion <- c(datapoints$congestion, x[i,6])
		i <- i+1
	}

	firstrow <- cbind(firstrow, c=toJSON(datapoints)[[1]])


	# result <- rbind(result, firstrow)
	write.table(firstrow, "result.csv", row.names=F, col.names=F, sep=",", append=T)

	# Reset
	firstrow <- x[i,c(2,7)]
	names(firstrow) <- c('a', 'b')
	initnode <- x[i,2]
	datapoints <- list(pml=x[i,3], energia= x[i,4], perdidas= x[i,5], congestion= x[i,6])
}

cat("\a")

