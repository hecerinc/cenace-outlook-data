
files <- list.files(pattern="^2018.*")
xx <- lapply(files, function(filename) {
	x <- read.csv(filename, header=F, stringsAsFactors=F)
	ax <- unlist(strsplit(filename, split="\\."))
	ax <- ax[1]
	ax <- gsub("_", "-", ax, fixed=TRUE)
	x$fecha <- ax
	write.table(x, filename, row.names=F, col.names=F, sep=",")
	rm(x)
});
cat("\a")

