import argparse
import glob
import os
from scipy.spatial.distance import cdist
import h5py
import numpy as np

def remove_black_hashes(hashes, frame_paths):
    indeces = np.where(np.all(hashes == 0, axis=1))
    hashes = hashes[~np.all(hashes == 0, axis=1)]
    frame_paths = np.delete(frame_paths, indeces)
    return hashes, frame_paths

def zero_pad_nr(frame_nr, len_number=6):
    len_frame_nr = len(str(frame_nr))
    len_padding = len_number - len_frame_nr
    new_nr = ('0'*len_padding) + str(frame_nr)
    return new_nr

def pad_movie_name(movie_name):
    n = movie_name.split('_')[0]
    new_n = zero_pad_nr(int(n), len_number=2)
    old_name = movie_name.split('_')[1]
    new_name = new_n + '_' + old_name
    return new_name


def remove_intro_outro_trailer(config, trailer_hashes, trailer_fns):
    trailer_length = config.trailer_length * 60
    trailer_hashes = trailer_hashes[60: trailer_length + 60]
    trailer_fns = trailer_fns[60: trailer_length + 60]
    return trailer_hashes, trailer_fns

def remove_intro_outro_movie(movie_hashes, movie_fns):
    movie_hashes = movie_hashes[60:-300]
    movie_fns = movie_fns[60:-300]
    return movie_hashes, movie_fns

def get_file_name(config, movie_name):
    file_name = 'distances_{}.hdf5'.format(movie_name)
    if config.rb:
        rb = 'rb_'
    else:
        rb = ''
    if config.rio:
        rio = 'rio_'
    else:
        rio = ''
    file_name = '{}{}{}'.format(rb, rio, file_name)
    return file_name

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
        distances_wd = home + 'distances/' + pad_movie_name(movie_name) +'/'

        print(hash_dir, distances_wd)

        try:
            os.mkdir(distances_wd)
        except:
            pass


        file_name = get_file_name(config, movie_name)
        distances_store = h5py.File(distances_wd + file_name, 'a')

        hash_datasets = [d for d in traverse_datasets(hash_file) if d.endswith('hashes')]
        frame_nr_datasets = [d for d in traverse_datasets(hash_file) if d.endswith('frames')]

        for i in range(0, len(hash_datasets)):

            hash_ds = hash_datasets[i]
            ds_name = hash_ds.replace('hashes', 'distances')

            fn_ds = frame_nr_datasets[i]

            if hash_ds not in distances_store:

                movie_hashes = hashes_store[hash_ds]
                movie_fns = hashes_store[fn_ds]

                trailer_hashes = hashes_store[hash_ds]
                trailer_fns = hashes_store[fn_ds]

                if config.rio:
                    movie_hashes, movie_fns = remove_intro_outro_movie(movie_hashes, movie_fns)
                    trailer_hashes, trailer_fns = remove_intro_outro_trailer(config, trailer_hashes, trailer_fns)
                else:
                    raise NotImplementedError

                if config.rb:
                    movie_hashes, movie_fns = remove_black_hashes(movie_hashes)
                    trailer_hashes, trailer_fns = remove_black_hashes(trailer_hashes)

                distances = cdist(movie_hashes, trailer_hashes, 'hamming')
                movie_fns, trailer_fns = np.meshgrid(movie_fns, trailer_fns, sparse=False, indexing='ij')

                distances_store.create_dataset(ds_name, data=distances, compression='gzip')
                distances_store.create_dataset(fn_ds + '/movie_fns', data=movie_fns, compression='gzip')
                distances_store.create_dataset(fn_ds + '/trailer_fns', data=trailer_fns, compression='gzip')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    parser.add_argument('--rb', type=bool, default=False, help='remove hashes of black frames')
    parser.add_argument('--rio', type=bool, default=True, help='remove intro and outro')
    config = parser.parse_args()
    get_distances_and_write(config)
