import os
from tqdm.auto import tqdm
import geopandas as gpd
import glob
import pyimpute
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import pickle

dir_path = os.path.dirname(os.path.realpath(__file__))

filetype = 'geojson'
species_list = ['Anser_albifrons', 'Haliaeetus_leucocephalus', 'Numenius_americanus', 'Numenius_phaeopus', 'Setophaga_striata']

def load_data(species, n=None):
      # Load species data
      pa_raw = gpd.GeoDataFrame.from_file(dir_path + '/input/geojson/' + species + '.' + filetype)

      if n:
            sample_size = n
            pa = pa_raw.sample(n=sample_size, random_state=1)
      else: 
            pa = pa_raw

      # Load climate data
      raster_features = sorted(glob.glob(dir_path + '/input/historical/*.tif'))

      # Load training vectors
      train_xs, train_y = pyimpute.load_training_vector(pa, raster_features, response_field='CLASS')

      # Remove NaN rows (why do they exist?)
      df = pd.DataFrame(train_xs)
      row_index = df.index[df.isna().any(axis=1)].tolist()
      print("NaN Rows:", row_index)

      train_xs = np.delete(train_xs, row_index, axis=0)
      train_y = np.delete(train_y, row_index, axis=0)

      return train_xs, train_y

for species in tqdm(species_list):
      X, y = load_data(species)

      # Create extra trees models
      model = RandomForestClassifier()

      # K-fold Cross Validation
      k = 5
      kf = model_selection.KFold(n_splits=k)
      accuracy_scores = model_selection.cross_val_score(model, X, y, cv=kf, scoring='accuracy')
      print(species + " %d-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)"
            % (k, accuracy_scores.mean() * 100, accuracy_scores.std() * 200))

      # Fit Model
      model.fit(X, y)

      os.makedirs(dir_path + '/../data/models/', exist_ok=True)
      pickle_filename = species + '_rf_classifier_model.pkl'
      pickle.dump(model, open(dir_path + "/../data/models/" + pickle_filename, 'wb'))