import numpy as np
import h5py
import os
import pandas as pd
from get_distances.traverse_datasets import traverse_datasets

#TODO: what to do about black frames ruining the minimum distance?

def get_min_max(paths, config = None):

    df_original = pd.DataFrame
    for path in paths:
        df = min_max_distances(path, config)
        df_original = pd.concat([df_original, df])

    return df_original

def min_max_distances(distances_path, config = None):
    """
    calculate min max distances per movie
    :param distances_path: path to hdf5 file with distances
    :param config: length trailer in minutes
    :return: pandas dataframe: {moviename, hashtype, max_s, min_s, max_ds, min_ds}
    """

    if config == None:
        len_trailer = 1
    else:
        len_trailer = config.trailer_length * 5

    movie_name = distances_path.split('/')[-2]
    distances_store = h5py.File(distances_path, 'a')
    datasets = [d for d in traverse_datasets(distances_path)]

    min_max_df = pd.DataFrame
    maxs_similar = []
    mins_similar = []
    maxs_dissimilar = []
    mins_dissimilar = []

    for dataset in datasets:
        distances = distances_store[dataset][:]
        similar = distances[:len_trailer,:]
        dissimilar = distances[len_trailer:,]
        maxs_similar.append(np.amax(similar))
        mins_similar.append(np.amin(similar))
        maxs_dissimilar.append(np.amax(dissimilar))
        mins_dissimilar.append(np.amin(dissimilar))

    min_max_df['hash_type'] = datasets
    min_max_df['max_similar'] = maxs_similar
    min_max_df['min_similar'] = mins_similar
    min_max_df['max_dissimilar'] = maxs_dissimilar
    min_max_df['min_dissimilar'] = mins_dissimilar
    movie_names = [movie_name] * len(datasets)
    min_max_df['movie_name'] = movie_names

    return min_max_df


