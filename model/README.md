# Usage

## Data pre-processing 

### R installation

1. Install R from https://cran.r-project.org/bin/windows/base/
2. (Optional) Install RStudio from https://posit.co/download/rstudio-desktop/
    - RStudio makes debugging easier, as you can view variables, run lines
      seperately, and run an instance of R cmd 

### Library dependencies

`data-pre-processing.R` requires four libraries: `raster`, `dismo`, `sf`, and
`geodata`

#### RStudio
1. Open `data-pre-processing.R`
2. Set working directory by going to **Session > Set Working Directory > To source file location**
3. Install packages by going to **Tools > Install packages**
    - Under *Install from:*, use *Repository* for each of the listed packages
    - Alternatively, type into console:
    ```
    install.packages(c("sf", "raster", "dismo", "geodata"))
    ```

### Using `data-pre-processing.R`
1. Ensure the desired .csv is saved under `model/data/` with the filename format `GBIF_[scientific name].csv`
2. In `data-pre-processing.R`,
    - change value for `filename` to `[scientific name]`
    - change value for `e` to desired latitude longitude
3. Run file, all output is saved in `model/data/` under respective folders
