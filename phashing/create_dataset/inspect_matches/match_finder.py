import numpy as np
import pickle
import argparse
import glob
import os
import h5py
from typing import List

class MatchFinder:

    def __init__(self, distances_paths: List[str]):
        self.distances_file_paths = distances_paths

        self.threshold = 0.35
        self.min_distance = False
        self.dataset = '/unaugmented/DCT_hash/DCTHash/12'

        self.matches = {}

    def set_distances_paths(self, distances_paths: List[str]):
        self.distances_file_paths = distances_paths

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_datasets(self, file_path):
        ds_names = [ds_name for ds_name in self.__traverse_datasets__(file_path)]
        datasets = list(set(['/'.join(d.split('/')[:-1]) for d in ds_names]))
        return datasets

    def get_incorrect_matches(self, save_matches=False, output_path=''):

        for path in self.distances_file_paths:

            distances, movie_fns, trailer_fns = self.__get_datasets__(path)

            distances_match, match_movie_fns, match_trailer_fns = self.__get_matches__(distances, movie_fns, trailer_fns)

            movie_name = path.split('/')[-2]
            print('getting matches of movie {}'.format(movie_name))

            self.matches[movie_name] = {}

            self.matches[movie_name]['distances'] = distances_match
            self.matches[movie_name]['movie_fns'] = match_movie_fns
            self.matches[movie_name]['trailer_fns'] = match_trailer_fns

        if save_matches:
            self.__save__(output_path)


    def __get_matches__(self, distances, movie_fns, trailer_fns,):

        if self.min_distance:
            minimum_distances = np.amin(distances, axis=1)
            i_trailer_minimum = np.argmin(distances, axis=1)
            i_movie_match = np.where(minimum_distances < self.threshold)[0]
            distances_match = minimum_distances[minimum_distances < self.threshold]
            i_trailer_match = i_trailer_minimum[i_movie_match]

        else:
            distances_match = distances[distances < self.threshold]
            matches = np.where(distances < self.threshold)
            i_movie_match, i_trailer_match = matches

        match_movie_fns = movie_fns[i_movie_match, i_trailer_match]
        match_trailer_fns = trailer_fns[i_movie_match, i_trailer_match]

        return (distances_match, match_movie_fns, match_trailer_fns)

    def __save__(self, output_path):
        threshold = str(self.threshold).replace('.', '')
        name_file = 'matches_{}.pickle'.format(threshold)
        path_file = os.path.join(output_path, name_file)
        with open(path_file, 'wb') as handle:
            pickle.dump(self.matches, handle)

    def __get_datasets__(self, path):

        file = h5py.File(path, 'r')
        ds_name_distances = os.path.join(self.dataset, 'distances')
        ds_name_movie_fns = os.path.join(self.dataset, 'movie_fns')
        ds_name_trailer_fns = os.path.join(self.dataset, 'trailer_fns')

        distances = file[ds_name_distances][:]
        movie_fns = file[ds_name_movie_fns][:]
        trailer_fns = file[ds_name_trailer_fns][:]

        return distances, movie_fns, trailer_fns

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


    def __get_hash_type__(self, dataset_name):
        parts_name = dataset_name.split('/')
        for part_name in parts_name:
            if 'hash' in part_name.lower():
                return part_name



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', type=bool, default=True, help='save incorrect matches')
    config = parser.parse_args()

    drive = '/movie-drive/'

    distances_folders = glob.glob(os.path.join(drive, 'distances') + '/*')
    distances_file_paths = [glob.glob(distances_folder + '/*')[0] for distances_folder in distances_folders]

    distances_file_paths = sorted(distances_file_paths)
    output_path = os.path.join(drive, 'results')

    match_finder = MatchFinder(distances_paths=distances_file_paths)

    datasets = match_finder.get_datasets(distances_file_paths[0])
    dataset = datasets[0]
    match_finder.set_dataset(dataset)
    print(match_finder.dataset)

    for threshold in [0.1, .15, .2, .25, .3, .35, .4]:
        match_finder.set_threshold(threshold)
        match_finder.get_incorrect_matches(save_matches=True, output_path=output_path)
