import argparse
import glob
import pickle
import numpy as np
from scipy.spatial.distance import cdist
import h5py
from create_dataset.hashing.hash_functions import DCT_hash, AVG_hash

def get_distances_and_write(hash_method, aug_method):

    distances_store = h5py.File('distances_aug.hdf5', 'a')

    loc = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/'

    with open(loc + 'aug_hashes/{}/{}_hashes.pickle'.format(hash_method.__name__, None), 'rb') as handle:
        phashes = np.array(pickle.load(handle))

    with open(loc + 'aug_hashes/{}/{}_hashes.pickle'.format(hash_method.__name__, aug_method), 'rb') as handle:
        phashes_aug_dict = pickle.load(handle)

    for ssid, phashes_aug in phashes_aug_dict.items():
        distances = cdist(phashes, np.array(phashes_aug), 'hamming')
        distances_store.create_dataset('{}/{}/{}'.format(hash_method.__name__, aug_method, ssid), data=distances, compression='gzip')


if __name__ == "__main__":
    hash_methods = [AVG_hash, DCT_hash]
    aug_methods = ['add_hsv', 'subtract_hsv', 'add', 'gauss', 'compress', 'contrast', 'subtract']
    for hash_method in hash_methods:
        for aug_method in aug_methods:
            get_distances_and_write(hash_method, aug_method)
