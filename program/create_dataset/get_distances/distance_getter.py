import argparse
import glob
import os
from scipy.spatial.distance import cdist
import h5py
import numpy as np
import typing
from typing import List

class DistanceGetter:

    def __init__(self, distances_dir:str, trailers_hashes_paths: List[str], movies_hashes_paths: List[str], remove_black_hashes=False):
        self.distances_dir = distances_dir
        self.__create_dir__(self.distances_dir)
        self.movies_hashes_paths = movies_hashes_paths
        self.trailer_hashes_paths = trailers_hashes_paths
        self.hashes_paths = list(zip(movies_hashes_paths, trailers_hashes_paths))

        self.ds_name_movie = '/unaugmented/DCTHash/12/'
        self.ds_name_trailer = '/unaugmented/DCTHash/12/'
        self.distances_ds_name = self.__create_ds_name__()

        self.remove_black_hashes=remove_black_hashes

    def get_dataset_names(self, h5py_path):
        return [d for d in self.__traverse_datasets__(h5py_path)]

    def get_distances_and_write(self):

        for movie_hashes_path, trailer_hashes_path in self.hashes_paths:
            movie_hashes, movie_fns = self.__get_datasets__(movie_hashes_path, self.ds_name_movie)
            trailer_hashes, trailer_fns = self.__get_datasets__(trailer_hashes_path, self.ds_name_trailer)

            if self.remove_black_hashes:
                movie_hashes, movie_fns = self.__remove_black_hashes__(movie_hashes, movie_fns)
                trailer_hashes, trailer_fns = self.__remove_black_hashes__(trailer_hashes, trailer_fns)

            movie_name = movie_hashes_path.split('/')[-2]

            distances_dir = os.path.join(self.distances_dir, movie_name)
            self.__create_dir__(distances_dir)

            store_name = self.__create_store_name__(movie_name)
            store_path = os.path.join(distances_dir, store_name)
            distances_store = h5py.File(store_path, 'a')

            if self.distances_ds_name not in distances_store:

                distances = cdist(movie_hashes, trailer_hashes, 'hamming')
                movie_fns, trailer_fns = np.meshgrid(movie_fns, trailer_fns, sparse=False, indexing='ij')

                distances_store.create_dataset(self.distances_ds_name + '/distances', data=distances, compression='gzip')
                distances_store.create_dataset(self.distances_ds_name + '/movie_fns', data=movie_fns, compression='gzip')
                distances_store.create_dataset(self.distances_ds_name + '/trailer_fns', data=trailer_fns, compression='gzip')

    def __create_dir__(self, dir):
        if os.path.exists(dir):
            pass
        else:
            os.mkdir(dir)

    def __get_datasets__(self, h5py_path, ds_name):
        hashes_store = h5py.File(h5py_path, 'r')
        ds_hashes = hashes_store[ds_name + 'hashes']
        ds_frame_numbers = hashes_store[ds_name + 'frames']
        return ds_hashes, ds_frame_numbers

    def __remove_black_hashes__(self, hashes, frame_paths):
        indeces = np.where(np.all(hashes == 0, axis=1))
        hashes = hashes[~np.all(hashes == 0, axis=1)]
        frame_paths = np.delete(frame_paths, indeces)
        return hashes, frame_paths

    def __create_store_name__(self, movie_name):
        file_name = 'distances_{}.hdf5'.format(movie_name)
        if self.remove_black_hashes:
            rb = 'rb_'
        else:
            rb = ''
        file_name = '{}{}'.format(rb, file_name)
        return file_name

    def __traverse_datasets__(self, hdf_file):
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

    def __create_ds_name__(self):
        movie_aspects = self.ds_name_movie.split('/')
        trailer_aspects = self.ds_name_trailer.split('/')
        distances_aspects = trailer_aspects
        for aspect in movie_aspects:
            if aspect not in trailer_aspects:
                index = movie_aspects.index(aspect)
                distances_aspects.insert(index, aspect)
        distances_ds_name = '/'.join(distances_aspects)
        return distances_ds_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--rb', type=bool, default=False, help='remove hashes of black frames')
    config = parser.parse_args()

    if config.VM:
        drive = '/movie-drive/'
    else:
        drive = os.path.join(os.getenv('HOME'), 'movie-drive')

    hashes_dir = os.path.join(drive, 'hashes')
    trailer_hashes_dir = os.path.join(drive, 'trailer_hashes')

    hashes_dirs = glob.glob(hashes_dir + '/*')
    trailer_hashes_dirs = glob.glob(trailer_hashes_dir + '/*')

    hashes_paths = [glob.glob(dir + '/*')[0] for dir in hashes_dirs]
    trailer_hashes_paths = [glob.glob(dir + '/*')[0] for dir in trailer_hashes_dirs]

    trailer_ns = sorted([t.split('/')[-2].split('_')[0] for t in trailer_hashes_paths]) 
    
    cleaned_hashes_paths = []
    
    for path in hashes_paths:
        print(path)
        movie_ns = path.split('/')[-2].split('_')[0]
        print(movie_ns)
        if movie_ns in trailer_ns:
            cleaned_hashes_paths.append(path)

    print(cleaned_hashes_paths)
    distances_wd = os.path.join(drive, 'distances')

    distance_getter = DistanceGetter(distances_dir= distances_wd, trailers_hashes_paths=sorted(cleaned_hashes_paths),
                                     movies_hashes_paths=sorted(trailer_hashes_paths), remove_black_hashes=config.rb)

    distance_getter.get_distances_and_write()
