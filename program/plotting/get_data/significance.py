import numpy as np
import h5py
import os
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

from traverse_datasets import traverse_datasets
from read_distances import read_distances
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

f_value, p_value = stats.f_oneway(data1, data2, data3, data4, ...)
result = pairwise_tukeyhsd(Data, Group)


data = np.rec.array([
    ('Pat', 5),
    ('Pat', 4),
    ('Pat', 4),
    ('Pat', 3),
    ('Pat', 9),
    ('Pat', 4),
    ('Jack', 4),
    ('Jack', 8),
    ('Jack', 7),
    ('Jack', 5),
    ('Jack', 1),
    ('Jack', 5),
    ('Alex', 9),
    ('Alex', 8),
    ('Alex', 8),
    ('Alex', 10),
    ('Alex', 5),
    ('Alex', 10)], dtype=[('Archer', '|U5'), ('Score', '<i8')])


print(data)
print(data.shape)

f, p = stats.f_oneway(data[data['Archer'] == 'Pat'].Score,
                      data[data['Archer'] == 'Jack'].Score,
                      data[data['Archer'] == 'Alex'].Score)

print('One-way ANOVA')
print('=============')

print('F value:', f)
print('P value:', p, '\n')

mc = MultiComparison(data['Score'], data['Archer'])
result = mc.tukeyhsd()

print(result)
print(mc.groupsunique)

def get_significance_data(distances_path):

    # movie_name = distances_path.split('/')[-2]

    distances_store = h5py.File(distances_path, 'a')
    datasets = [d for d in traverse_datasets(distances_path)]

    dist_avg_4 = np.array()
    dist_avg_6 = np.array()
    dist_avg_10

    for dataset in datasets:
        distances_matrix = distances_store[dataset][:]


    kruskall_wallis_df['hash_type'] = datasets
    kruskall_wallis_df['max_similar'] = maxs_similar
    kruskall_wallis_df['min_similar'] = mins_similar
    kruskall_wallis_df['max_dissimilar'] = maxs_dissimilar
    kruskall_wallis_df['min_dissimilar'] = mins_dissimilar
    movie_names = [movie_name] * len(datasets)
    kruskall_wallis_df['movie_name'] = movie_names

    return kruskall_wallis_df


def histogram_occurences(distances_store, dataset, len_trailer, min_distance = False):

    similar, dissimilar = read_distances(distances_store, dataset, len_trailer, min_distance=False)


    hist_sim = np.histogram(similar, range=(0,1))
    values = hist_sim[0]
    bins = hist_sim[1][:-1]
    hist_sim = np.vstack((values, bins))

    hist_dissim = np.histogram(dissimilar, range=(0,1))
    values = hist_dissim[0]
    bins = hist_dissim[1][:-1]
    hist_dissim = np.vstack((values, bins))

    return hist_sim, hist_dissim