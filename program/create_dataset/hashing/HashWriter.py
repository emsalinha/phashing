import time
import h5py
import numpy as np
import os
import glob
import argparse

class HashWriter:

    def __init__(self, config):
        self.config = config
        self.home = str()
        self.__import_modules__()
        self.hash_params = {
            'method': None,
            'augmentation': False,
            'hash_size': None,
            'high_freq_factor': 8,
            'vertical': 0,
            'horizontal': 0
        }
        self.hasher = None
        self.hash_methods = []
        self.hash_sizes = [4, 8, 12]

        self.fps = 25
        self.ds_name_frames = str()
        self.ds_name_hashes = str()
        self.frame_dirs = sorted(glob.glob(self.home + 'frames/*'))
        self.speed_per_hash = 0
        self.speed_csv = open(self.home + 'results/speed_hashing_new.csv', 'w')


    def import_modules(self):
        if self.config.VM:
            self.home = '/movie-drive/'
            from Hasher import Hasher
            self.hasher = Hasher()
        else:
            self.home = os.getenv('HOME') + '/movie-drive/'
            from create_dataset.hashing.Hasher import Hasher
            self.hasher = Hasher()


    def hash_and_write(self):

        for frame_dir in self.frame_dirs:

            frame_paths = sorted(glob.glob(frame_dir + '/*'))
            self.frame_paths = frame_paths[0::self.fps]

            self.movie_name = frame_paths[0].split('/')[-2]
            hashes_wd = self.home + 'hashes/' + movie_name

            try:
                os.mkdir(hashes_wd)
                os.chdir(hashes_wd)
            except:
                continue

            for hash_method in self.hasher.hash_methods:
                for hash_size in self.hash_sizes:

                    self.hash_params['hash_size'] = hash_size
                    self.hash_params['hash_method'] = hash_method
                    self.get_ds_names()
                    self.hash_and_write()

                    hash_construction = '{}_{}'.format(hash_method.__name__, hash_size)
                    self.speed_csv.write('{}: {}: {}\n'.format(movie_name, hash_construction, self.speed))

        self.speed_csv.close()

    def get_ds_names(self):
        if self.hash_params['augmentation']:
            group_name = 'augmented'
        else:
            group_name = 'unaugmented'
        subgroup_name = self.hash_params['hash_method'].__name__
        subsubgroup_name = self.hash_params['hash_size']
        self.ds_name_hashes = '{}/{}/{}/hashes'.format(group_name, subgroup_name, subsubgroup_name)
        self.ds_name_frames = '{}/{}/{}/frames'.format(group_name, subgroup_name, subsubgroup_name)

    def get_ds_sizes(self, frame_paths):

        hash_len = self.hash_params['hash_size'] * self.hash_params['hash_size']
        n_frames = len(frame_paths)

        ds_size_hashes = (n_frames, hash_len)
        ds_size_fps = (n_frames,)
        return ds_size_hashes, ds_size_fps

    def create_h5py_stores(self):
        ds_size_hashes, ds_size_fps = self.get_ds_sizes(self.frame_paths)
        hdf5_store = h5py.File('annotated_hashes_{}.hdf5'.format(self.movie_name), 'a')
        phashes_ds = hdf5_store.create_dataset(self.ds_name_hashes, ds_size_hashes, compression='gzip')
        dt = h5py.special_dtype(vlen=np.dtype('int32'))
        frame_paths_ds = hdf5_store.create_dataset(self.ds_name_frames, ds_size_fps, dtype=dt)
        return phashes_ds, frame_paths_ds

    def hash_and_write(self):
        """
        writes hashes one by one to a (newly created) HDF5 file in the working directory
        :param movie_name: 'movie name'
        :param frame_paths: [paths to frames in movie]
        :param hash_method: DCT or average hash
        :param hash_params: {augmentation, hash_size, high_freq_factor, vertical, horizontal}
        :param fps: sampled frames per second
        :return time spend per hash
        :output hdf5 file: /augmentation/hash_method/hash_size
        """
        print(self.ds_name_hashes)

        phashes_ds, frame_paths_ds = self.create_h5py_stores()

        n_frames = len(self.frame_paths)

        start = time.time()

        for i in range(0, n_frames):

            phash = self.hasher.hash(self.frame_paths[i], self.hash_params)
            phashes_ds[i] = phash

            frame_nr = self.frame_paths[i].split('/')[-1].split('_')[1].split('.')[0]
            frame_paths_ds[i] = [int(frame_nr)]

        end = time.time()
        self.speed_per_hash = (end-start)/n_frames


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
	config = parser.parse_args()
	hasher = HashWriter(config)
