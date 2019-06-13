import numpy as np
import h5py
import os
import pandas as pd
import argparse
import glob

#TODO: what to do about black frames ruining the minimum distance?

def get_min_max(paths, config):

    df_original = pd.DataFrame()
    for path in paths:
        df = min_max_distances(path, config)
        df_original = pd.concat([df_original, df])

    return df_original

def min_max_distances(distances_path, config):
    """
    calculate min max distances per movie
    :param distances_path: path to hdf5 file with distances
    :param config: length trailer in minutes
    :return: pandas dataframe: {moviename, hashtype, max_s, min_s, max_ds, min_ds}
    """

    if config.VM:
        home = '/movie-drive/'
        from utils.traverse_datasets import traverse_datasets
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from get_data.extract_data.utils.traverse_datasets import traverse_datasets

    n_frames_trailer = config.trailer_length * 60


    movie_name = distances_path.split('/')[-2]
    distances_store = h5py.File(distances_path, 'a')
    datasets = [d for d in traverse_datasets(distances_path)]

    min_max_df = pd.DataFrame()
    maxs_similar = []
    mins_similar = []
    maxs_dissimilar = []
    mins_dissimilar = []

    for dataset in datasets:
        distances = distances_store[dataset][:]
        n_frames_trailer = distances.shape[1]
        trailer = distances[:n_frames_trailer,:]
        rest = distances[n_frames_trailer:,]
        diagonal = np.eye(trailer.shape[0], dtype=bool)
        dissimilar = trailer[~diagonal].reshape(diagonal.shape[0]-1, diagonal.shape[0])
        dissimilar = np.vstack((dissimilar, rest))
        similar = trailer[diagonal]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    home = os.getenv('HOME') + '/movie-drive/'
    distance_dirs = sorted(glob.glob(home + 'results/distances/*'))
    distances_paths = [glob.glob(distance_dir + '/*')[0] for distance_dir in distance_dirs]

    min_max_distances(distances_paths[0], config)

    #write_hists_occurences(result_dir, distances_paths, config)


