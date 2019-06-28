import glob
import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from matplotlib import rc
from get_distances.traverse_datasets import traverse_datasets

def undo_pad_nr(frame_nr):
    if frame_nr[0] == '0':
        frame_nr = frame_nr[1]
    return frame_nr

def zero_pad_nr(frame_nr, len_number=6):
    len_frame_nr = len(str(frame_nr))
    len_padding = len_number - len_frame_nr
    new_nr = ('0'*len_padding) + str(frame_nr)
    return new_nr

def read_distances(path, i):
    distances = h5py.File(path, 'r')
    datasets = []
    for dataset in traverse_datasets(path):
        datasets.append(dataset)
    return datasets[i], np.array(distances[datasets[i]])


def get_similar_dissimilar(distances_matrix, len_trailer, min_distance=True):
    if min_distance:
        distances = np.amin(distances_matrix, axis=1)
        indeces = np.argmin(distances_matrix, axis=1)

        dissimilar = distances[len_trailer:]
        dissimilar_indeces = indeces[len_trailer:]
    else:
        dissimilar = distances_matrix[len_trailer:, :]
        dissimilar_indeces = None

    return dissimilar_indeces, dissimilar


def get_wrong_hashes(distances_paths_c2, ds, save=False):
    wrong_hashes = {}

    for i in range(0, len(ds)):
        d = ds[i].split('/')[-2] + '_' + ds[i].split('/')[-1]
        wrong_hashes[d] = {}

        for path in distances_paths_c2:
            name = path.split('distances_')[1].split('.')[0]

            dataset, distances = read_distances(path, i)

            dissimilar_indeces, dissimilar = get_similar_dissimilar(distances, len_trailer=300)
            #incorrect_dissimilar = dissimilar[dissimilar<0.05]
            indexes_video = np.where(dissimilar < 0.05)[0]

            indexes_trailer = dissimilar_indeces[indexes_video]

            wrong_hashes[d][name] = (indexes_video, indexes_trailer)

    if save:
        with open('wrong_hashes_new.pickle', 'wb') as handle:
            pickle.dump(wrong_hashes, handle)

    return wrong_hashes

movies = sorted(glob.glob('/home/emsala/movie-drive/distances/*'))
distances_paths_c2 = [sorted(glob.glob(movie + '/*'))[0] for movie in movies]

datasets = []
for dataset in traverse_datasets(distances_paths_c2[0]):
    datasets.append(dataset)
datasets = sorted(datasets)

wh = get_wrong_hashes(distances_paths_c2, datasets, save=True)
