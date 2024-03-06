library(sf)
library(raster)
library(dismo)
library(geodata)

# MODIFY THESE PARAMETERS FOR EACH DATAFILE

filename <- "CardellinaPusilla" # set filename
e <- extent(-124, -114, 32, 42) # set study area extent

# pipe GBIF data
jt_raw <- read.csv(paste('data/GBIF_', filename, '.csv', sep = ""),
                   header = TRUE, sep = '\t')
jt_raw <- jt_raw[which(jt_raw$countryCode=='US'),] # restrict to US
jt <- data.frame(matrix(ncol = 2, nrow = length(jt_raw$decimalLongitude)))
jt[,1] <- jt_raw$decimalLongitude
jt[,2] <- jt_raw$decimalLatitude
jt <- unique(jt) # xantusia without duplicates
jt <- jt[complete.cases(jt),] # remove na's
colnames(jt) <- c('lon','lat')

# crop species data to wanted region
jt <- jt[which(jt$lon>=e[1] & jt$lon<=e[2]),] # remove presences beyond extent
jt <- jt[which(jt$lat>=e[3] & jt$lat<=e[4]),] # remove presences beyond extent

# grab climate data using geodata
bioclim.data <- worldclim_global(var = "bio",
                                 path = "data/",
                                 res = 2.5,
                                 version = "2.1")
bioclim.data <- stack(bioclim.data)
bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent

# write rasters to /data folder
for (i in c(1:19)){
  writeRaster(bioclim.data[[i]], 
           paste('data/bioclim/bclim', i, '.asc', sep = ''),
           overwrite = TRUE)
}

## ------------------------------------------------------------------------

# Trim jt
jt_trim <- jt[sample(nrow(jt), 2000), ]
length_presences <- nrow(jt_trim)

# sample background points from a slightly wider extent
bg <- randomPoints(bioclim.data[[1]], length_presences*2, ext=e, extf = 1.25)
colnames(bg) <- c('lon','lat')
train <- rbind(jt_trim, bg)  # combine with presences
pa_train <- c(rep(1, nrow(jt_trim)), rep(0, nrow(bg))) # col of ones and zeros
train <- data.frame(cbind(CLASS=pa_train, train)) # final dataframe
 
# create spatial points
train <- train[sample(nrow(train)),]
dataMap.sf <- st_as_sf(train,
                       coords = c('lon', 'lat'),
                       crs = 4326)

# write as geojson
st_write(dataMap.sf, 
         paste('data/geojson/', filename, '.geojson', sep = ""),
         append = FALSE,
         delete_dsn = TRUE)

# plot our points
plot(bioclim.data[[1]], main='Bioclim 1')
points(bg, col='red', pch = 16,cex=.3)
points(jt_trim, col='black', pch = 16,cex=.3)
plot(wrld_simpl, add=TRUE, border='dark grey')
