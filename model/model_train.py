import os
from tqdm.auto import tqdm
import geopandas as gpd
import glob
from pyimpute import load_training_vector
from pyimpute import load_targets
from pyimpute import impute
from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
import pandas as pd
import pickle

filetype = 'geojson'
species_list = ['Anser_albifrons', 'Haliaeetus_leucocephalus', 'Numenius_americanus', 'Numenius_phaeopus', 'Setophaga_striata']

for species in tqdm(species_list):
    # Load species data
    pa_raw = gpd.GeoDataFrame.from_file('data/geojson/' + species + '.' + filetype)

    sample_size = 20000
    pa = pa_raw.sample(n=sample_size, random_state=1)

    # Load climate data
    raster_features = sorted(glob.glob('data/MIROC6/historical/*.asc'))

    # Load training vectors
    train_xs, train_y = load_training_vector(pa, raster_features, response_field='CLASS')

    # Remove NaN rows (why do they exist?)
    df = pd.DataFrame(train_xs)
    row_index = df.index[df.isna().any(axis=1)].tolist()
    print("NaN Rows:", row_index)

    train_xs = np.delete(train_xs, row_index, axis=0)
    train_y = np.delete(train_y, row_index, axis=0)

    # Load target vectors
    target_xs, raster_info = load_targets(raster_features)

    # Create random forest models
    model = ExtraTreesClassifier()

    k = 5
    kf = model_selection.KFold(n_splits=k)
    accuracy_scores = model_selection.cross_val_score(model, train_xs, train_y, cv=kf, scoring='accuracy')
    print("extra-trees %d-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)"
          % (k, accuracy_scores.mean() * 100, accuracy_scores.std() * 200))
    
    model.fit(train_xs, train_y)
    os.makedirs('outputs/models/', exist_ok=True)
    filename = species + '_et_classifier_model.pkl'
    pickle.dump(model, open('outputs/models/' + filename, 'wb'))