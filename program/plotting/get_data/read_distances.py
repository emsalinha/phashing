import numpy as np

def read_distances(distances_store, dataset, len_trailer, min_distance = True):
    distances_matrix = distances_store[dataset][:]

    if min_distance:
        distances = np.amin(distances_matrix, axis=1)
        similar = distances[:len_trailer]
        dissimilar = distances[len_trailer:]
    else:
        distances = distances_matrix
        similar = distances[:len_trailer, :]
        dissimilar = distances[len_trailer:, :]

    return similar, dissimilar
