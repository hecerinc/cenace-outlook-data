library(dplyr)

# missing <- c("03ARN-115", "04ECC-400", "01KMC-85", "02BGB-115", "02CLX-115", "02THP-400", "02TMZ-69", "03B21-115", "03B24-115", "03J06-69", "03N06-115", "03P3M-115", "03S12-115", "04SSA-230", "05NAC-115", "05PH2-115", "06CUF-138", "06ILP-115", "06PTN-115", "02BEN-115", "02GEP-115")
missing <- c("07DAR-69", "07RZD-161", "07SF2-115", "07TJI-230")

files <- list.files(pattern="^2017.*")

xx <- lapply(files, function(filename) {
	x <- read.csv(filename, header=F, stringsAsFactors=F)
	y <- dplyr::filter(x, V2 %in% missing)
	x <- dplyr::filter(x, !(V2 %in% missing))
	ax <- unlist(strsplit(filename, split="\\."))
	ax <- ax[1]
	write.table(y, paste(ax, "_missing.csv", sep=""), row.names=F, col.names=F, sep=",")
	write.table(x, filename, row.names=F, col.names=F, sep=",")
	rm(x, y)
});

