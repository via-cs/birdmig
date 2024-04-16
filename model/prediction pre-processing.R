library(sf)
library(raster)
library(dismo)
library(geodata)

e <- extent(-124, -114, 32, 42) # set study area extent

# grab climate data using geodata
filename <-'data/future/wc2.1_2.5m_bioc_MIROC6_ssp126_2021-2040.tif' 
bioclim.data = raster(filename)
bioclim.data <- stack(bioclim.data)
bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent

# write rasters to /data folder
for (i in c(1:19)){
  writeRaster(bioclim.data[[i]], 
           paste('data/future/21-40/bclim', i, '.asc', sep = ''),
           overwrite = TRUE)
}
