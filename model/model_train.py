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

filetype = 'geojson'
species_list = ['Anser_albifrons', 'Haliaeetus_leucocephalus', 'Numenius_americanus', 'Numenius_phaeopus', 'Setophaga_striata']

def load_data(species, n):
      # Load species data
      pa_raw = gpd.GeoDataFrame.from_file('data/geojson/' + species + '.' + filetype)

      sample_size = n
      pa = pa_raw.sample(n=sample_size, random_state=1)

      # Load climate data
      raster_features = sorted(glob.glob('data/MIROC6/historical/*.tif'))

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
      X, y = load_data(species, 20000)

      # Create extra trees models
      model = RandomForestClassifier()

      # K-fold Cross Validation
      k = 5
      kf = model_selection.KFold(n_splits=k)
      accuracy_scores = model_selection.cross_val_score(model, X, y, cv=kf, scoring='accuracy')
      print("extra-trees %d-fold Cross Validation Accuracy: %0.2f (+/- %0.2f)"
            % (k, accuracy_scores.mean() * 100, accuracy_scores.std() * 200))

      # Fit Model
      model.fit(X, y)

      #pyimpute.evaluate_clf(model, train_xs, train_y)

      os.makedirs('outputs/models/', exist_ok=True)
      filename = species + '_et_classifier_model.pkl'
      pickle.dump(model, open('outputs/models/' + filename, 'wb'))