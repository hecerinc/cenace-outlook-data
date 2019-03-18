files <- list.files(pattern="^2017.*")
wholeyear <- do.call(rbind, lapply(files, function(x) read.csv(x, header=F)))

wholeyear <- wholeyear$V2
writeLines(as.character(levels(wholeyear)), "nodesBCS.txt")

