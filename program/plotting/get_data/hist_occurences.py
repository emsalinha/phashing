from traverse_datasets import traverse_datasets
from read_distances import read_distances
import h5py
import argparse
import numpy as np
import os
import glob

#TODO: which values (dims) of distances should I put in the np histogram?
# how to loop and add over nunmpy histogram
#TODO: config None -> len_trailer x 5???

def write_hists_occurences(results_dir, distances_paths, config = None):
    """
    creates histogram per movie, per hashtype, per distribution (similar vs non-simalar)
    :param distances_paths: path to all distances files
    :param config: config.len_trailer: to know which distances belong to similar or dissimilar frames
    :return: None
    :output: histograms_moviename.hdf5 dataset: hist_similar, hist_dissimilar, groups: augmentation/hash_method/hash_size/
    """

    if config == None:
        len_trailer = 1
    else:
        len_trailer = config.trailer_length * 5

    for distances_path in distances_paths:
        movie_name = distances_path.split('/')[-2]
        distances_store = h5py.File(distances_path, 'a')
        datasets = [d for d in traverse_datasets(distances_path)]

        histogram_store = h5py.File(results_dir + 'hists_{}.hdf5'.format(movie_name), 'a')
        histograms_occurences(histogram_store, distances_store, datasets, len_trailer)


def histograms_occurences(histogram_store, distances_store, datasets, len_trailer):
    for dataset in datasets:
        hist_sim, hist_dissim = histogram_occurences(distances_store, dataset, len_trailer)
        ds_s = dataset + '/hist_similar'
        ds_d = dataset + '/hist_dissimilar'
        histogram_store.create_dataset(ds_s, data=hist_sim, compression='gzip')
        histogram_store.create_dataset(ds_d, data=hist_dissim, compression='gzip')

def histogram_occurences(distances_store, dataset, len_trailer):
    similar, dissimilar = read_distances(distances_store, dataset, len_trailer, min_distance = True)

    hist_sim = np.histogram(similar, range=(0,1))
    values = hist_sim[0]
    bins = hist_sim[1][:-1]
    hist_sim = np.vstack((values, bins))

    hist_dissim = np.histogram(dissimilar, range=(0,1))
    values = hist_dissim[0]
    bins = hist_dissim[1][:-1]
    hist_dissim = np.vstack((values, bins))

    return hist_sim, hist_dissim


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    home = os.getenv('HOME') + '/movie-drive/'
    distance_dirs = sorted(glob.glob(home + 'distances/*'))
    distances_paths = [glob.glob(distance_dir + '/*')[0] for distance_dir in distance_dirs]
    result_dir = home + 'results/'

    write_hists_occurences(result_dir, distances_paths, config)
