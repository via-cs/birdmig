library(sf)
library(raster)
library(dismo)
library(geodata)
library(ncdf4)

# Parameters
species_list <- list("Anser_albifrons",
                     "Haliaeetus_leucocephalus",
                     "Numenius_americanus",
                     "Numenius_phaeopus",
                     "Setophaga_striata")
export_filetype <- "geojson"
e <- extent(-179, -50, 7, 65) # set study area extent to Americas

# Grab Climate Data
bioclim.data <- stack(raster("data/MIROC6/raw/historical/temperature_2014.nc"),
                      raster("data/MIROC6/raw/historical/precipitation_2014.nc"))
bioclim.data <- rotate(bioclim.data, left=TRUE) # convert (0, 360) to (-180, 180)
bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent

# pipe GBIF data
for (s in species_list) {
  s = "Anser_albifrons"
  jt_raw <- read.csv(paste('data/GBIF_', s, '.csv', sep = ""),
                     header = TRUE, sep = '\t')
  jt <- data.frame(matrix(ncol = 2, nrow = length(jt_raw$decimalLongitude)))
  jt[,1] <- jt_raw$decimalLongitude
  jt[,2] <- jt_raw$decimalLatitude
  jt <- unique(jt) # xantusia without duplicates
  jt <- jt[complete.cases(jt),] # remove na's
  colnames(jt) <- c('lon','lat')
  
  # crop species data to wanted region
  jt <- jt[which(jt$lon>=e[1] & jt$lon<=e[2]),] # remove presences beyond extent
  jt <- jt[which(jt$lat>=e[3] & jt$lat<=e[4]),] # remove presences beyond extent
  
  # Trim jt
  #jt_trim <- jt[sample(nrow(jt), length(bioclim.data[[1]])), ]
  length_presences <- nrow(jt)
  
  # sample background points from a slightly wider extent
  bg <- randomPoints(bioclim.data[[1]], length_presences, ext=e, extf = 1.25)
  colnames(bg) <- c('lon','lat')
  train <- rbind(jt, bg)  # combine with presences
  pa_train <- c(rep(1, length_presences), rep(0, nrow(bg))) # col of ones and zeros
  train <- data.frame(cbind(CLASS=pa_train, train)) # final dataframe
  
  # create spatial points
  train <- train[sample(nrow(train)),]
  dataMap.sf <- st_as_sf(train,
                         coords = c('lon', 'lat'),
                         crs = 4326)
  
  # write as geojson
  st_write(dataMap.sf, 
           paste('data/', export_filetype, '/', s, '.', export_filetype,
                 sep = ""),
           append = FALSE,
           delete_dsn = TRUE)
}

## ------------------------------------------------------------------------

# plot our points
plot(bioclim.data[[1]], main='Precipitation')
points(bg, col='red', pch = 16,cex=.3)
points(jt, col='black', pch = 16,cex=.3)
plot(wrld_simpl, add=TRUE, border='dark grey')


writeRaster(bioclim.data[[1]], 
            paste('data/MIROC6/historical/temperature.asc', sep = ''),
            overwrite = TRUE)

writeRaster(bioclim.data[[2]], 
            paste('data/MIROC6/historical/precipitation.asc', sep = ''),
            overwrite = TRUE)
