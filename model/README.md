# Usage

Before running the SDM, data must be preprocessed into a form factor fit for model training and prediction.

## R Preprocessing 

### R installation

1. Install R from https://cran.r-project.org/bin/windows/base/
2. Install RStudio from https://posit.co/download/rstudio-desktop/
    - RStudio makes debugging easier, as you can view variables, run lines
      seperately, and run an instance of R cmd 
    - Alternatively, install the Rscript package for command line use

### Library dependencies

These R scripts require four libraries: `raster`, `dismo`, `sf`, and
`ncdf4`

1. Open `preprocessing-train.R`
2. Set working directory by going to **Session > Set Working Directory > To source file location**
3. Install packages by going to **Tools > Install packages**
    - Under *Install from:*, use *Repository* for each of the listed packages
    - Alternatively, type into console:
    ```
    install.packages(c("sf", "raster", "dismo", "ncdf4"))
    ```

### Getting the data
Data can be found in the included Box folder at [this link](https://ucdavis.app.box.com/s/l5iky1y6z526r6ewifvtr6c4ccp5jsjz). This
folder includes the species CSV's used for this project, the climate datasets indexed by year and SSP, and a script for processing migration patterns (see the technical document under `techdoc/tech-doc.pdf`).

To use this data, download the `/data` folder from the above link and place it
in the root directory of this repository after cloning.

If a different species is desired, download the CSV from GBIF and
place in the `/data/` folder like so:

    /data/GBIF/[scientific name].csv
    
### Training preprocessing
Ensure that the climate and desired species datasets are placed according to
the above section
    
1. In `preprocessing_train.R`,
    - Include [scientific name] in `species_list`
        - Alternatively, replace all names by [scientific name] if you only want
          the one processed
    - change value for `e` to desired latitude & longitude (default set to
      Americas)
    
3. Run script (in RStudio) 

All output is saved in `/model/input/geojson/` and `/model/input/historical/`
for species and climate data respectively. The data is now ready for training
the model.

### Prediction preprocessing
Ensure that the future climate datasets are placed according to
the above section. These can be downloaded from the Box folder.
    
1. In `preprocessing_predict.R`,
    - change value for `e` to desired latitude & longitude (default set to
      Americas)
    
3. Run script (in RStudio) 

All output is saved in `/model/input/future` for future climate data. The data
is now ready for use for prediction (see section model_prediction.py)

## The Species Distribution Model
If the required data is correctly preprocessed (see above), then these scripts should be easily run in any terminal:

```
python3 model/model_train.py
python3 model/model_predict.py
```

These commands can be run seperately if the necessary preprocessed data exists. For more information, see the technical document at `/techdoc/tech-doc.pdf`