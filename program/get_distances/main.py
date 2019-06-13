import argparse
import glob
import os
from scipy.spatial.distance import cdist
import h5py
import numpy as np

def remove_black_hashes(hashes):
    hashes = hashes[~np.all(hashes == 0, axis=1)]
    return hashes


def get_distances_and_write(config):

    if config.VM:
        home = '/movie-drive/'
        from traverse_datasets import traverse_datasets
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from get_distances.traverse_datasets import traverse_datasets

    hash_dirs = sorted(glob.glob(home + 'hashes/*'))

    for hash_dir in hash_dirs:

        hash_file = glob.glob(hash_dir + '/*')[0]
        hashes_store = h5py.File(hash_file, 'r')


        movie_name = hash_file.split('/')[-2]
        distances_wd = home + 'distances/' + movie_name +'/'

        trailer_length = config.trailer_length*60

        try:
            os.mkdir(distances_wd)
        except:
            continue

        if config.remove_black_hashes:
            distances_store = h5py.File(distances_wd + 'clean_distances_{}.hdf5'.format(movie_name), 'a')
        else:
            distances_store = h5py.File(distances_wd + 'distances_{}.hdf5'.format(movie_name), 'a')

        hash_datasets = [dataset for dataset in traverse_datasets(hash_file)]

        for hash_dataset in hash_datasets:
            if hash_dataset not in distances_store:
                movie_hashes = hashes_store[hash_dataset][60:-300]
                trailer_hashes = hashes_store[hash_dataset][60:trailer_length+60]
                if config.remove_black_hashes:
                    movie_hashes = remove_black_hashes(movie_hashes)
                    trailer_hashes = remove_black_hashes(trailer_hashes)
                distances = cdist(movie_hashes, trailer_hashes, 'hamming')
                distances_store.create_dataset(hash_dataset, data=distances, compression='gzip')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    parser.add_argument('--remove_black_hashes', type=bool, default=True, help='remove hashes of black frames')
    config = parser.parse_args()
    get_distances_and_write(config)
