# Usage

Before running the SDM, data must be preprocessed into a form factor fit for model training and prediction.

## R Preprocessing 

### R installation

1. Install R from https://cran.r-project.org/bin/windows/base/
2. Install RStudio from https://posit.co/download/rstudio-desktop/
    - RStudio makes debugging easier, as you can view variables, run lines
      seperately, and run an instance of R cmd 

### Library dependencies

These R scripts requires four libraries: `raster`, `dismo`, `sf`, and
`ncdf4`

1. Open `training-preprocessing.R`
2. Set working directory by going to **Session > Set Working Directory > To source file location**
3. Install packages by going to **Tools > Install packages**
    - Under *Install from:*, use *Repository* for each of the listed packages
    - Alternatively, type into console:
    ```
    install.packages(c("sf", "raster", "dismo", "ncdf4"))
    ```

### Getting the data
Data can be found in the included Box folder at **[insert link here]**. This
data includes the species CSV's used for this project, as well as the climate
datasets indexed by year and SSP.

To use this data, download the `/data` folder from the above link and place it
in the root directory of this repository after cloning.

If a different species is desired, download the CSV from GBIF and
place in the `/data/` folder like so:

    /data/GBIF/[scientific name].csv
    
### Training preprocessing
Ensure that the climate and desired species datasets are placed according to
the above section
    
1. In `training-preprocessing.R`,
    - Include [scientific name] in `species_list`
        - Alternatively, replace all names by [scientific name] if you only want
          the one processed
    - change value for `e` to desired latitude & longitude (default set to
      Americas)
    
3. Run script (in RStudio) 

All output is saved in `/model/input/geojson/` and `/model/input/historical/`
for species and climate data respectively. The data is now ready for training
the model (see section model_train.py)

### Prediction preprocessing
Ensure that the future climate datasets are placed according to
the above section. These can be downloaded from the Box folder.
    
1. In `prediction-preprocessing.R`,
    - change value for `e` to desired latitude & longitude (default set to
      Americas)
    
3. Run script (in RStudio) 

All output is saved in `/model/input/future` for future climate data. The data
is now ready for use for prediction (see section model_prediction.py)

## Running the SDM

1. Open `birdmid-sdm.ipynb`
2. Ensure you are running a version of python that supports pip installation
   (for example, Anaconda3)
3. Run all cells
    - Everything required by model should be in the github
    - Necessary files can always be procured by running `data-pre-processing.R`
      with necessary input files
