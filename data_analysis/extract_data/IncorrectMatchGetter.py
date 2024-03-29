import numpy as np
import pickle
import argparse
import glob
import os
from typing import List

from get_data.extract_data.utils.traverse_datasets import traverse_datasets, read_ds


class IncorrectMatchGetter:

    def __init__(self, config):
        self.config = config
        self.threshold = 0.5
        self.min_distance = True
        self.len_trailer = self.config.len_trailer * 60
        self.drive = self.get_drive()
        self.incorrect_matches = {}
        self.distances_file_paths = self.get_distances_file_paths()
        self.distances_ds_names, self.movie_fns_ds_names, self.trailer_fns_ds_names = self.get_dataset_names()

        self.movie_fns_ds = None
        self.trailer_fns_ds = None
        self.distances_ds = None

        self.non_matching_distances = None
        self.non_matching_movie_fns = None
        self.non_matching_trailer_fns = None

        self.incorrect_matches_fns = tuple()

        self.get_incorrect_matches()
        self.save()

    def get_drive(self):
        if self.config.VM:
            drive = '/movie-drive/'
        else:
            drive = os.getenv('HOME') + '/movie-drive/'
        return drive

    def save(self):
        if self.config.save:
            name_file = 'incorrect_matches_{}.pickle'.format(str(self.threshold)[:-2])
            with open('{}results/incorrect_matches/{}'.format(self.drive, name_file), 'wb') as handle:
                pickle.dump(self.incorrect_matches, handle)


    def get_distances_file_paths(self):
        distances_folders = glob.glob(self.drive + 'distances/*')
        distances_file_paths = [glob.glob(distances_folder + '/*')[0] for distances_folder in distances_folders]
        distances_file_paths = sorted(distances_file_paths)
        return distances_file_paths

    def get_incorrect_matches(self):

        for i in range(0, len(self.distances_ds_names)):

            hash_type = self.get_hash_type(self.distances_ds_names[i])
            print(hash_type)
            self.incorrect_matches[hash_type] = {}

            for distances_file_path in self.distances_file_paths:

                movie_name = distances_file_path.split('/')[-1].split('distances_')[-1].split('.')[0]
                print(movie_name)

                self.movie_fns_ds = read_ds(distances_file_path, self.movie_fns_ds_names[i])
                self.trailer_fns_ds = read_ds(distances_file_path, self.trailer_fns_ds_names[i])
                self.distances_ds = read_ds(distances_file_path, self.distances_ds_names[i])

                self.get_non_matching_ds()

                incorrect_matches_movie = self.get_incorrectly_matched()

                if hash_type.endswith('8') or hash_type.endswith('12'):
                    print(incorrect_matches_movie)

                self.incorrect_matches[hash_type][movie_name] = incorrect_matches_movie

    def get_dataset_names(self):
        file_path = self.distances_file_paths[0]
        ds_names = [ds_name for ds_name in traverse_datasets(file_path)]
        distances_ds_names = [ds_name for ds_name in ds_names if ds_name.endswith('distances')]
        movie_fns_ds_names = [ds_name for ds_name in ds_names if ds_name.endswith('movie_fns')]
        trailer_fns_ds_names = [ds_name for ds_name in ds_names if ds_name.endswith('trailer_fns')]
        return distances_ds_names, movie_fns_ds_names, trailer_fns_ds_names


    def get_hash_type(self, dataset_name):
        return dataset_name.split('/')[-3] + '_' + dataset_name.split('/')[-2]


    def get_non_matching_ds(self):
        self.non_matching_distances = self.distances_ds[self.len_trailer:]
        self.non_matching_movie_fns = self.movie_fns_ds[self.len_trailer:]
        self.non_matching_trailer_fns = self.trailer_fns_ds[self.len_trailer:]

    def get_incorrectly_matched(self):

        if self.min_distance:
            minimum_distances = np.amin(self.non_matching_distances, axis=1)
            i_trailer_minimum = np.argmin(self.non_matching_distances, axis=1)
            i_movie_incorrect_match = np.where(minimum_distances < self.threshold)[0]
            incorrect_distances = minimum_distances[minimum_distances < self.threshold]
            i_trailer_incorrect_match = i_trailer_minimum[i_movie_incorrect_match]

        else:
            incorrect_matches = np.where(self.non_matching_distances < self.threshold)
            i_movie_incorrect_match, i_trailer_incorrect_match = incorrect_matches

        incorrect_fnm = self.non_matching_movie_fns[i_movie_incorrect_match, i_trailer_incorrect_match]
        incorrect_fnt = self.non_matching_trailer_fns[i_movie_incorrect_match, i_trailer_incorrect_match]

        if not incorrect_fnm.shape[0] == 0:
            if incorrect_fnt.max() > incorrect_fnm.min():
                raise IndexError

        return (incorrect_fnm, incorrect_fnt, incorrect_distances)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--len_trailer', type=int, default=5, help='trailer length in minutes')
    parser.add_argument('--save', type=bool, default=True, help='save incorrect matches')
    # parser.add_argument('--rb', type=bool, default=False, help='remove hashes of black frames')
    # parser.add_argument('--rio', type=bool, default=False, help='remove intro and outro')
    config = parser.parse_args()

    match_getter = IncorrectMatchGetter(config)
