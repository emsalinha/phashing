import numpy as np
import pickle
import argparse
import glob
import os


def get_dissimilar(distances, fpm, fpt, len_trailer):
    dis_dist = distances[len_trailer:]
    dis_fpm = fpm[len_trailer:]
    dis_fpt = fpt[len_trailer:]
    return dis_dist, dis_fpm, dis_fpt

def get_incorrect_fns(dis_dist, dis_fpm, dis_fpt, min_distance=True):

    if min_distance:

        min_dist = np.amin(dis_dist, axis=1)
        i_trailer = np.argmin(dis_dist, axis=1)
        i_movie = np.where(min_dist < 0.05)[0]
        i_trailer = i_trailer[i_movie]

    else:
        i_movie, i_trailer = np.where(dis_dist < 0.05)

    incorrect_fpm = dis_fpm[i_movie, i_trailer]
    incorrect_fpt = dis_fpt[i_movie, i_trailer]
    incorrect_matches = list(zip(incorrect_fpm, incorrect_fpt))

    return incorrect_matches

def clean_name(dataset):
    return dataset.split('/')[-3] + '_' + dataset.split('/')[-2]

def get_datasets(file_path):
    ds = [d for d in traverse_datasets(file_path)]
    ds_distances = [d for d in ds if d.endswith('hashes')]
    ds_movie_fns = [d for d in ds if d.endswith('movie_fns')]
    ds_trailer_fns = [d for d in ds if d.endswith('trailer_fns')]
    return ds_distances, ds_movie_fns, ds_trailer_fns

def save_incorrect_matches(distances_paths, len_trailer, home, min_distance=True, save=False):

    all_incorrect_matches = {}

    ds_distances,_,_ = get_datasets(distances_paths[0])
    ds_distances = [clean_name(ds) for ds in ds_distances]

    for i in range(0, len(ds_distances)):

        hash_type = ds_distances[i]
        all_incorrect_matches[hash_type] = {}

        for path in distances_paths:

            movie_name = path.split('/')[-1].split('distances_')[-1].split('.')[0]
            print(movie_name)

            ds_name, fpm_ds = read_distances(path, i)
            ds_name, fpt_ds = read_distances(path, i + 1)
            ds_name, distances_ds = read_distances(path, i + 2)

            assert(hash_type == clean_name(ds_name), "Incorrect indexing of hash type")
            print(hash_type, clean_name(ds_name))

            dis_dist, dis_fpm, dis_fpt = get_dissimilar(distances_ds, fpm_ds, fpt_ds, len_trailer=len_trailer)
            incorrect_matches = get_incorrect_fns(dis_dist, dis_fpm, dis_fpt, min_distance=min_distance)
            print(incorrect_matches)

            all_incorrect_matches[hash_type][movie_name] = incorrect_matches

    if save:
        with open('{}results/incorrect_matches.pickle'.format(home), 'wb') as handle:
            pickle.dump(all_incorrect_matches, handle)

    return all_incorrect_matches

def main(config):

    if config.VM:
        from utils.traverse_datasets import read_distances
        from utils.traverse_datasets import traverse_datasets
        len_trailer = config.len_trailer * 60
        home = '/movie-drive/'

    else:
        from get_data.extract_data.utils.traverse_datasets import read_distances
        from get_data.extract_data.utils.traverse_datasets import traverse_datasets
        len_trailer = config.len_trailer
        home = os.getenv('HOME') + '/movie-drive/'

    distances_folders = home + 'results/distances'
    distances_paths = [sorted(glob.glob(distances_folder + '/*'))[0] for distances_folder in distances_folders]

    matches = save_incorrect_matches(distances_paths, len_trailer, home)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--len_trailer', type=int, default=5, help='trailer length in minutes')
    # parser.add_argument('--rb', type=bool, default=False, help='remove hashes of black frames')
    # parser.add_argument('--rio', type=bool, default=False, help='remove intro and outro')
    config = parser.parse_args()

    main(config)
