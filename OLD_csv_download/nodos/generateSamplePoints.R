sink("output2.txt", type=c("output"))
library(sp)
library(rgdal)
library(dplyr)

dirs <- list.dirs(".", recursive=FALSE)

# Read nodes
nodes <- read.csv("nodos.csv", header=TRUE, stringsAsFactors=FALSE)
estados <- c("AGUASCALIENTES", "BAJA CALIFORNIA", "BAJA CALIFORNIA SUR", "CAMPECHE", "COAHUILA", "COLIMA", "CHIAPAS", "CHIHUAHUA", "CD.MEXICO", "DURANGO", "GUANAJUATO", "GUERRERO", "HIDALGO", "JALISCO", "ESTADO DE MEXICO", "MICHOACAN", "MORELOS", "NAYARIT", "NUEVO LEON", "OAXACA", "PUEBLA", "QUERETARO", "QUINTANA ROO", "SAN LUIS POTOSI", "SINALOA", "SONORA", "TABASCO", "TAMAULIPAS", "TLAXCALA", "VERACRUZ", "YUCATAN", "ZACATECAS")

CRS.new <- CRS("+init=epsg:4326")

result <- do.call(rbind, lapply(dirs, function(dirname) {
	setwd("~/mapping")
	setwd(dirname)
	setwd("conjunto de datos/")
	dirname <- substring(dirname, 3)
	num <- unlist(strsplit(dirname, "_"))[1]
	num <- strtoi(num, base=10L)
	hasprinted <- FALSE
	nodesinstate <- dplyr::filter(nodes, ESTADO == estados[num])
	if(nrow(nodesinstate) == 0) {

		print(paste("ESTADO FAIL:", dirname, num))
		print(estados[num])
		return(data.frame())
	}
	nodesinstate$location.long <- NA 
	nodesinstate$location.lat <- NA 

	# Read shapefile
	x <- readOGR(dsn=".", layer=paste(sprintf("%02d", num), "mun", sep=""))
	x <- spTransform(x, CRS.new)


	# ISSUE: names in NOMGEO have accents but the ones in the nodes list do not
	# Replacements:
	# a tilde: \u00E1
	# e tilde: \u00E9
	# i tilde: \u00ED
	# o tilde: \u00F3
	# u tilde: \u00FA

	x$NOMGEO <- as.character(x$NOMGEO)
	nombres <- x$NOMGEO
	nombres <- tolower(nombres)
	nombres <- gsub("\u00E1", "a", nombres, fixed=TRUE)
	nombres <- gsub("\u00E9", "e", nombres, fixed=TRUE)
	nombres <- gsub("\u00ED", "i", nombres, fixed=TRUE)
	nombres <- gsub("\u00F3", "o", nombres, fixed=TRUE)
	nombres <- gsub("\u00FA", "u", nombres, fixed=TRUE)
	x$NOMGEO <- nombres
	for (i in 1:nrow(nodesinstate)) {
		city <- trimws(tolower(nodesinstate[i, "LOCALIDAD"]))
		cityShape <- x[x$NOMGEO == city,]
		if(nrow(cityShape) == 0) {
			if(!hasprinted){
				print(x$NOMGEO)
				hasprinted = TRUE
			}
			print(paste("FAILED:", city))
			next
		}

		# Get the sample point matrix (1 by 2)
		sample_point <- coordinates(spsample(cityShape, n = 1, "random", iter=10))
		nodesinstate[i, "location.long"] <- sample_point[1,1] # x
		nodesinstate[i, "location.lat"] <- sample_point[1,2] # y
	}
	rm(i)
	return(nodesinstate[!is.na(nodesinstate$location.lat),]);
}))
print("FINISHED!")
setwd("~/mapping")
write.csv(result, "result.csv", row.names=FALSE)


