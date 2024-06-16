import os
from tqdm.auto import tqdm
import glob
from pyimpute import load_targets
from pyimpute import impute
import pickle
import rasterio
from matplotlib.pylab import plt

dir_path = os.path.dirname(os.path.realpath(__file__))

species_list = ['Anser_albifrons', 'Haliaeetus_leucocephalus', 'Numenius_americanus', 'Numenius_phaeopus', 'Setophaga_striata']
year_list = list(range(2015, 2101))
ssp_list = ["ssp126", "ssp245", "ssp370", "ssp585"]

def make_prediction(species, ssp, year):
    raster_features = sorted(glob.glob(dir_path + '/input/future/' + ssp + '/' + str(year) + '/*.tif'))

    target_xs, raster_info = load_targets(raster_features)

    pickle_filename = species + "_rf_classifier_model.pkl"
    model = pickle.load(open(dir_path + "/../data/models/" + pickle_filename, 'rb'))

    os.makedirs(dir_path + '/output/tiff-images/' + species + '/' + ssp + '/' + str(year), exist_ok=True)
    impute(target_xs, model, raster_info, outdir= dir_path + '/output/tiff-images/' + species + '/' + ssp + '/' + str(year),
            class_prob=True, certainty=True)
                
def create_pngs(species, ssp, year):
    distr = rasterio.open(dir_path + '/output/tiff-images/' + species + '/' + ssp + '/' + str(year) + '/probability_1.0.tif').read(1)

    fig = plt.figure(frameon=False)
    fig.set_size_inches(4,4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(distr, cmap="Greens", interpolation='nearest', aspect='auto')
    
    os.makedirs(dir_path + '/../public/png-images/' + species + '/' + ssp, exist_ok=True)
    fig.savefig(dir_path + '/../public/png-images/' + species + '/' + ssp + '/' + str(year) + '.png', dpi = 200)

    plt.close(fig)

for species in tqdm(species_list, desc="Species"):
    for ssp in tqdm(ssp_list, desc="ssp"):
        for year in tqdm(year_list, desc="Years"):
            make_prediction(species, ssp, year)
            create_pngs(species, ssp, year)