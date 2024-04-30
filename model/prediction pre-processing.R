library(sf)
library(raster)
library(dismo)
library(geodata)

e <- extent(-179, -35, -55, 85) # set study area extent to Americas

ssp_list <- list ("ssp126", "ssp245", "ssp370", "ssp585")
year_list <- list("2021-2040", "2041-2060", "2061-2080")

for (s in ssp_list) {
  for (y in year_list) {
    # grab climate data using geodata
    filename <- paste('data/future/wc2.1_2.5m_bioc_MIROC6_', s, "_", y, '.tif', sep='')
    bioclim.data <- stack(filename)
    options(scipen=999) # avoid scientific notation
    bioclim.data <- crop(bioclim.data, e*1.25)  # crop to bg point extent

    # write rasters to /data folder
    for (i in c(1:19)){
      writeRaster(bioclim.data[[i]],
                  paste('data/future/', y, '/', s, '/bclim', i, '.asc', sep = ''),
                  overwrite = TRUE)
    }
  }
}
