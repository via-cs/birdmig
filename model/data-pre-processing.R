#' ---
#' title: "sdms_data_piping"
#' author: "Daniel Furman"
#' date: "2020"
#' ---
#' 
#' This R script pipes presence and absence data for joshua trees
#' 
#' Data citation:
#' GBIF.org (01 November 2020) GBIF Occurrence
#' Download https://doi.org/10.15468/dl.g6swrm 
## ------------------------------------------------------------------------

library(raster)
library(dismo)
library(geodata)
library(rgdal)

## ------------------------------------------------------------------------

# pipe GBIF data
jt_raw <- read.csv("data/GBIF_CardellinaPusilla.csv", header = TRUE, sep = "\t") # grab GBIF
jt_raw <- jt_raw[which(jt_raw$countryCode=='US'),] # restrict to US
jt <- data.frame(matrix(ncol = 2, nrow = length(jt_raw$decimalLongitude)))
jt[,1] <- jt_raw$decimalLongitude
jt[,2] <- jt_raw$decimalLatitude
jt <- unique(jt) # xantusia without duplicates
jt <- jt[complete.cases(jt),] # remove na's
colnames(jt) <- c('lon','lat')

# download Bioclim features
e <- extent(-130,-110,32,42) # set study area extent (minLon, maxLon, minLat, maxLat)
jt <- jt[which(jt$lon>=e[1] & jt$lon<=e[2]),] # remove presences beyond extent
jt <- jt[which(jt$lat>=e[3] & jt$lat<=e[4]),] # remove presences beyond extent
# use dismo's getData to grab climate features
bioclim.data <- worldclim_global(var = "bio",
                                 res = 2.5,
                                 path = "data/",
                                 version = "2.1")
bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent
# write rasters to /data folder
for (i in c(1:19)){
  writeRaster(bioclim.data[[i]], paste('data/bclim', i, '.asc', sep = ''), overwrite = TRUE)
}

## ------------------------------------------------------------------------

# sample background points from a slightly wider extent
bg <- raptr::randomPoints(bioclim.data[[1]], n = 100)
colnames(bg) <- c('lon','lat')
train <- rbind(jt, bg)  # combine with presences
pa_train <- c(rep(1, nrow(jt)), rep(0, nrow(bg))) # col of ones and zeros
train <- data.frame(cbind(CLASS=pa_train, train)) # final dataframe

# create spatial points
crs <- crs(bioclim.data[[1]])
train <- train[sample(nrow(train)),]
class.pa <- data.frame(train[,1])
colnames(class.pa) <- 'CLASS'
dataMap.jt  <- SpatialPointsDataFrame(train[,c(2,3)], class.pa,
                                      proj4string = CRS())
# write as shp
#writeOGR(dataMap.jt, 'data/jtree.shp','jtree', driver='ESRI Shapefile')
st_write(dataMap.jt, "data/bird.shp")

# plot our points
plot(bioclim.data[[1]], main='Bioclim 1')
points(bg, col='red', pch = 16,cex=.3)
points(jt, col='black', pch = 16,cex=.3)
plot(wrld_simpl, add=TRUE, border='dark grey')
