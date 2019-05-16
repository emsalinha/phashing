from get_distances.traverse_datasets import traverse_datasets
import h5py
import pandas as pd
import numpy as np

#TODO: which values (dims) of distances should I put in the np histogram?
# how to loop and add over nunmpy histogram

def hist_occurences(distances_path, config = None):

    if config == None:
        len_trailer = 1
    else:
        len_trailer = config.trailer_length * 5

    movie_name = distances_path.split('/')[-2]
    distances_store = h5py.File(distances_path, 'a')
    datasets = [d for d in traverse_datasets(distances_path)]

    hist_sim = init_hist()
    hist_dissim = init_hist()

    for dataset in datasets:
        distances = distances_store[dataset][:]
        similar = distances[:len_trailer,:]
        dissimilar = distances[len_trailer:,]
        hist_sim += np.histogram(similar)
        hist_dissim += np.histogram(dissimilar)

    df_hists = convert_hist_to_df(movie_name, hist_sim, hist_dissim)
    return df_hists

def init_hist():
    pass


def convert_hist_to_df(movie_name, hist_sim, hist_dissim):
    pass
