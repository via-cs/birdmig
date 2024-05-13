import os
from tqdm.auto import tqdm
import glob
from pyimpute import load_targets
from pyimpute import impute
import pickle
import rasterio
from matplotlib.pylab import plt

species_list = ['Anser_albifrons', 'Haliaeetus_leucocephalus', 'Numenius_americanus', 'Numenius_phaeopus', 'Setophaga_striata']
year_list = list(range(2015, 2100))
ssp_list = ["ssp126", "ssp245", "ssp370", "ssp585"]

for species in tqdm(species_list, desc="Species"):
    for ssp in tqdm(ssp_list, desc="ssp"):
        for year in tqdm(year_list, desc="Years"):
            raster_features = sorted(glob.glob('data/MIROC6/' + ssp + '/' + str(year) + '/*.asc'))

            target_xs, raster_info = load_targets(raster_features)

            pickle_filename = "outputs/models/" + species + '_et_classifier_model.pkl'
            model = pickle.load(open(pickle_filename, 'rb'))

            os.makedirs('outputs/tiff-images/' + species + '/' + ssp + '/' + str(year), exist_ok=True)
            impute(target_xs, model, raster_info, outdir='outputs/tiff-images/' + species + '/' + ssp + '/' + str(year),
                    class_prob=True, certainty=True)
            
            distr = rasterio.open('outputs/tiff-images/' + species + '/' + ssp + '/' + str(year) + '/probability_1.0.tif').read(1)

            plt.imshow(distr, cmap="Greens", interpolation='nearest')
            os.makedirs('outputs/png-images/' + species + '/' + ssp, exist_ok=True)
            plt.savefig('outputs/png-images/' + species + '/' + ssp + '/' + str(year) + '.png', dpi=200, bbox_inches='tight')