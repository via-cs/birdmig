library(sf)
library(raster)
library(geodata)
library(ncdf4)
library(RNetCDF)

e <- extent(-179, -35, -55, 85) # set study area extent to Americas

ssp_list <- list ("ssp126", "ssp245", "ssp370", "ssp585")
year_list <- as.list(seq(2015,2100)) 
feature_list <- list ("tas", "pr")

for (s in ssp_list) {
  for (y in year_list) {
    for (f in feature_list) {
      # grab climate data using geodata
      filename <- paste('data/MIROC6/.netcd4/', s, '/r1i1p1f1/', f, 
                        '/', f, '_day_MIROC6_', s, '_r1i1p1f1_gn_', as.character(y), '.nc', sep='')
      bioclim.data <- raster(filename)
      bioclim.data <- rotate(bioclim.data, left=TRUE) # convert (0, 360) to (-180, 180)
      options(scipen=999) # avoid scientific notation
      bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent
  
      # write rasters to /data folder
      if (f == "pr") {
        file_save = "precipitation.asc"
      } else {
        file_save = "temperature.asc"
      }
      
      cidr <- getwd()
      subdr <- paste('data/MIROC6/', s, '/', y, sep='')
      dir.create(file.path(cidr, subdr), recursive = TRUE)
      
      writeRaster(bioclim.data,
                  paste(subdr, '/', file_save, sep = ''),
                  overwrite = TRUE)
    }
  }
}
