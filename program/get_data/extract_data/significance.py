import h5py
import os
from scipy import stats
import argparse
import numpy as np
import pandas as pd

from statsmodels.stats.multicomp import MultiComparison
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def get_significances(distances_all_movies_path, config):

    if config.VM:
        home = '/movie-drive/'
        from utils.traverse_datasets import traverse_datasets

    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from get_data.extract_data.utils.traverse_datasets import traverse_datasets

    distances_store = h5py.File(distances_all_movies_path, 'a')
    datasets = [d for d in traverse_datasets(distances_all_movies_path) if 'unaugmented' in d]

    data1 = distances_store[datasets[0]][:]
    names1 = np.array([datasets[0]] * data1.shape[0])
    data2 = distances_store[datasets[1]][:]
    names2 = np.array([datasets[1]] * data2.shape[0])
    data3 = distances_store[datasets[2]][:]
    names3 = np.array([datasets[2]] * data3.shape[0])
    data4 = distances_store[datasets[3]][:]
    names4 = np.array([datasets[3]] * data4.shape[0])
    data5 = distances_store[datasets[4]][:]
    names5 = np.array([datasets[4]] * data5.shape[0])
    data6 = distances_store[datasets[5]][:]
    names6 = np.array([datasets[5]] * data6.shape[0])

    f_value, p_value = stats.f_oneway(data1, data2, data3, data4, data5, data6)


    # print('One-way ANOVA')
    # print('=============')
    #
    # print('F value:', f_value)
    # print('P value:', p_value, '\n')

    data = np.hstack((data1, data2, data3, data4, data5, data6))
    names = np.hstack((names1, names2, names3, names4, names5, names6))
    mc = MultiComparison(data, names)
    result = mc.tukeyhsd()

    df_result = pd.DataFrame(data=result._results_table.data[1:], columns=result._results_table.data[0])

    df_anova = pd.DataFrame(data = [f_value, p_value], columns = ['f, p'])

    return df_result, df_anova



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    path = '/home/emsala/movie-drive/distances/all_movies/distances_all_movies.hdf5'
    get_significances(path, config)
