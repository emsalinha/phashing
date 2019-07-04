import argparse
import glob
import os
from scipy.spatial.distance import cdist
import h5py
import numpy as np


class DistanceGetter:

    def __init__(self, config):
        self.config = config
        self.drive = self.get_drive()
        self.hash_dirs = sorted(glob.glob(self.drive + 'hashes/*'))
        self.get_distances_and_write()

    def get_drive(self):
        if self.config.VM:
            drive = '/movie-drive/'
        else:
            drive = os.getenv('HOME') + '/movie-drive/'
        return drive


    def get_distances_and_write(self):

        for hash_dir in self.hash_dirs:

            hash_file = glob.glob(hash_dir + '/*')[0]
            hashes_store = h5py.File(hash_file, 'r')

            movie_name = hash_file.split('/')[-2]
            distances_wd = self.drive + 'distances/' + self.pad_movie_name(movie_name) + '/'

            print(hash_dir, distances_wd)

            try:
                os.mkdir(distances_wd)
            except:
                continue

            file_name = self.get_file_name(movie_name)
            distances_store = h5py.File(distances_wd + file_name, 'a')

            hash_datasets = [d for d in self.traverse_datasets(hash_file) if d.endswith('hashes')]
            frame_nr_datasets = [d for d in self.traverse_datasets(hash_file) if d.endswith('frames')]

            for i in range(0, len(hash_datasets)):

                hash_ds = hash_datasets[i]
                ds_name = hash_ds.replace('hashes', 'distances')

                fn_ds = frame_nr_datasets[i]

                if hash_ds not in distances_store:

                    movie_hashes = hashes_store[hash_ds]
                    movie_fns = hashes_store[fn_ds]

                    trailer_hashes = hashes_store[hash_ds]
                    trailer_fns = hashes_store[fn_ds]

                    if self.config.rio:
                        movie_hashes, movie_fns = self.remove_intro_outro_movie(movie_hashes, movie_fns)
                        trailer_hashes, trailer_fns = self.remove_intro_outro_trailer(self.config, trailer_hashes,
                                                                                 trailer_fns)
                    else:
                        raise NotImplementedError

                    if self.config.rb:
                        movie_hashes, movie_fns = self.remove_black_hashes(movie_hashes)
                        trailer_hashes, trailer_fns = self.remove_black_hashes(trailer_hashes)

                    distances = cdist(movie_hashes, trailer_hashes, 'hamming')
                    movie_fns, trailer_fns = np.meshgrid(movie_fns, trailer_fns, sparse=False, indexing='ij')

                    distances_store.create_dataset(ds_name, data=distances, compression='gzip')
                    distances_store.create_dataset(fn_ds + '/movie_fns', data=movie_fns, compression='gzip')
                    distances_store.create_dataset(fn_ds + '/trailer_fns', data=trailer_fns, compression='gzip')


    def remove_black_hashes(self, hashes, frame_paths):
        indeces = np.where(np.all(hashes == 0, axis=1))
        hashes = hashes[~np.all(hashes == 0, axis=1)]
        frame_paths = np.delete(frame_paths, indeces)
        return hashes, frame_paths

    def zero_pad_nr(self, frame_nr, len_number=6):
        len_frame_nr = len(str(frame_nr))
        len_padding = len_number - len_frame_nr
        new_nr = ('0'*len_padding) + str(frame_nr)
        return new_nr

    def pad_movie_name(self, movie_name):
        n = movie_name.split('_')[0]
        new_n = self.zero_pad_nr(int(n), len_number=2)
        old_name = movie_name.split('_')[1]
        new_name = new_n + '_' + old_name
        return new_name


    def remove_intro_outro_trailer(self, config, trailer_hashes, trailer_fns):
        trailer_length = config.trailer_length * 60
        trailer_hashes = trailer_hashes[60: trailer_length + 60]
        trailer_fns = trailer_fns[60: trailer_length + 60]
        return trailer_hashes, trailer_fns

    def remove_intro_outro_movie(self, movie_hashes, movie_fns):
        movie_hashes = movie_hashes[60:-300]
        movie_fns = movie_fns[60:-300]
        return movie_hashes, movie_fns

    def get_file_name(self, movie_name):
        file_name = 'distances_{}.hdf5'.format(movie_name)
        if self.config.rb:
            rb = 'rb_'
        else:
            rb = ''
        if self.config.rio:
            rio = 'rio_'
        else:
            rio = ''
        file_name = '{}{}{}'.format(rb, rio, file_name)
        return file_name


    def traverse_datasets(self, hdf_file):
        def h5py_dataset_iterator(g, prefix=''):
            for key in g.keys():
                item = g[key]
                path = f'{prefix}/{key}'
                if isinstance(item, h5py.Dataset):  # test for dataset
                    yield (path, item)
                elif isinstance(item, h5py.Group):  # test for group (go down)
                    yield from h5py_dataset_iterator(item, path)

        with h5py.File(hdf_file, 'r') as f:
            for path, _ in h5py_dataset_iterator(f):
                yield path


    def read_distances(self, path, i):
        hists = h5py.File(path, 'r')
        datasets = []
        for dataset in self.traverse_datasets(path):
            datasets.append(dataset)
        return datasets[i], np.array(hists[datasets[i]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    parser.add_argument('--rb', type=bool, default=False, help='remove hashes of black frames')
    parser.add_argument('--rio', type=bool, default=True, help='remove intro and outro')
    configuration = parser.parse_args()
    distance_getter = DistanceGetter(configuration)
