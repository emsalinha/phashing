import h5py
import os
import numpy as np
import glob
import argparse

def rewrite_distances(config):

    if config.VM:
        home = '/movie-drive/'
        from traverse_datasets import traverse_datasets
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from get_distances.traverse_datasets import traverse_datasets

    distance_dirs = sorted(glob.glob(home + 'distances/*'))
    distances_paths = [glob.glob(distance_dir + '/*')[0] for distance_dir in distance_dirs]
    init_datasets = [d for d in traverse_datasets(distances_paths[-5])]

    new_distances_dir = home + 'distances/all_movies/'
    os.mkdir(new_distances_dir)

    distances_all_store = h5py.File(new_distances_dir + 'distances_all_movies.hdf5', 'a')

    init_data = np.array([0.5])
    for init_dataset in init_datasets:
        distances_all_store.create_dataset(init_dataset, data=init_data, maxshape=(None,), compression='gzip')


    for distances_path in distances_paths:
        distances_store = h5py.File(distances_path, 'a')
        dataset_names = [d for d in traverse_datasets(distances_path)]

        for dataset_name in dataset_names:
            distances = np.amin(distances_store[dataset_name][:], axis=1).flatten()
            dataset = distances_all_store[dataset_name]
            new_shape = dataset.shape[0] + distances.shape[0]
            dataset.resize(new_shape, axis=0)
            print(dataset.shape)
            dataset[-distances.shape[0]:] = distances


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    rewrite_distances(config)
