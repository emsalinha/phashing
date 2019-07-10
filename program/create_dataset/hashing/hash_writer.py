import time
import h5py
import numpy as np
import os
import glob
import argparse
from typing import List
import typing
from hasher import Hasher, AVGHash,DCTHash

class HashWriter:

    def __init__(self, hasher: Hasher, frame_dir: str, hash_dir:str, log_path:str, load_img=True):
        self.ds_name_frames = str()
        self.ds_name_hashes = str()
        self.ds_size_hashes = (0, 0)
        self.ds_size_fps = (0, 0)

        self.fps = 1

        self.frame_dir = frame_dir
        self.frame_paths = sorted(glob.glob(self.frame_dir + '/*'))[::self.fps]
        self.load_img = load_img

        self.hasher = hasher
        self.__get_ds_names__()
        self.__get_ds_sizes__()


        self.movie_name = self.frame_dir.split('/')[-1]
        self.hash_dir = os.path.join(hash_dir, self.movie_name)
        self.__create_hash_dir__()
        self.h5py_file = os.path.join(self.hash_dir, 'hashes_{}.hdf5'.format(self.movie_name))

        self.speed_per_hash = 0
        self.speed_csv_path = os.path.join(log_path, 'speed_hashing.csv')

    def set_hasher(self, hasher: Hasher):
        self.hasher = hasher
        self.__get_ds_names__()
        self.__get_ds_sizes__()

    def set_fps(self, fps: int):
        self.fps = fps


    def write_hashes(self):

        self.speed_csv = open(self.speed_csv_path, 'w')

        phashes_ds, frame_paths_ds = self.__create_h5py_stores__()

        n_frames = len(self.frame_paths)

        start = time.time()

        for i in range(0, n_frames):

            phash = self.hasher.phash(self.frame_paths[i], load_img=self.load_img)
            phashes_ds[i] = phash

            frame_nr = self.__get_frame_nr__(self.frame_paths[i])
            frame_paths_ds[i] = [frame_nr]

        end = time.time()
        self.speed_per_hash = (end-start)/float(n_frames)

        self.__write_speed__()


    def __get_frame_nr__(self, frame_path):
        """
        :param frame_path: assume basename format : [path]/[frame]_[frame_nr].[ext]
        :return: frame_nr
        """
        base_name = os.path.basename(frame_path)
        base_name_no_ext = base_name.split('.')[0]
        frame_nr = base_name_no_ext.split('_')[1]
        return int(frame_nr)

    def __create_hash_dir__(self):
        if os.path.exists(self.hash_dir):
            pass
        else:
            os.mkdir(self.hash_dir)

    def __write_speed__(self):
        hash_construction = '{}_{}'.format(self.hasher.hash_params['hash_method'], self.hasher.hash_params['hash_size'])
        self.speed_csv.write('{}: {}: {}\n'.format(self.movie_name, hash_construction, self.speed_per_hash))
        self.speed_csv.close()

    def __get_ds_names__(self):
        if self.hasher.hash_params['augmentation'] == None:
            raise ValueError('Indicate in hash_params whether the image data is augmented')
        if self.hasher.hash_params['augmentation']:
            group_name = 'augmented'
        else:
            group_name = 'unaugmented'
        subgroup_name = self.hasher.hash_params['hash_method']
        subsubgroup_name = self.hasher.hash_params['hash_size']
        self.ds_name_hashes = '{}/{}/{}/hashes'.format(group_name, subgroup_name, subsubgroup_name)
        self.ds_name_frames = '{}/{}/{}/frames'.format(group_name, subgroup_name, subsubgroup_name)

    def __get_ds_sizes__(self):

        hash_size = self.hasher.hash_params['hash_size']
        hash_len = hash_size*hash_size
        n_frames = len(self.frame_paths)

        self.ds_size_hashes = (n_frames, hash_len)
        self.ds_size_fps = (n_frames,)

    def __create_h5py_stores__(self):
        hdf5_store = h5py.File(self.h5py_file, 'a')
        if self.ds_name_hashes in hdf5_store:
            raise FileExistsError('hash dataset already exists in hdf5 store')
        else:
            phashes_ds = hdf5_store.create_dataset(self.ds_name_hashes, self.ds_size_hashes, compression='gzip')
            dt = h5py.special_dtype(vlen=np.dtype('int32'))
            frame_paths_ds = hdf5_store.create_dataset(self.ds_name_frames, self.ds_size_fps, dtype=dt)
        return phashes_ds, frame_paths_ds


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    configuration = parser.parse_args()

    if configuration.VM:
        home = '/movie-drive/'
        from hasher import Hasher, AVGHash, DCTHash
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from create_dataset.hashing.hasher import Hasher, AVGHash, DCTHash

    frame_dirs = sorted(glob.glob(os.path.join(home, 'trailer_frames') +'/*'))
    hash_dir = os.path.join(home, 'hashes')
    log_path = os.path.join(home, 'results')


    dct_hasher = DCTHash()
    dct_hasher.hash_params['augmentation'] = False
    for frame_dir in frame_dirs:
        hash_writer = HashWriter(dct_hasher, frame_dir=frame_dir, hash_dir=hash_dir, log_path=log_path)
        print(hash_writer.movie_name)
        hash_writer.write_hashes()
