import argparse
import os
import glob
import numpy as np


def get_data_to_plot(config):

    if config.VM:
        home = '/movie-drive/'
        from min_max import get_min_max
        from f1_score_data import get_f1_score_data
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from plotting.get_data.min_max import get_min_max
        from plotting.get_data.f1_score_data import get_f1_score_data

    distance_dirs = sorted(glob.glob(home + 'distances/*'))
    distance_paths = [glob.glob(distance_dir + '/*')[0] for distance_dir in distance_dirs]
    result_dir = home + 'results/'

    df_min_max = get_min_max(distance_paths, config)
    df_min_max.to_pickle(result_dir + 'df_min_max.pkl')

    thresholds = np.arange(0, 1, 0.1)
    for threshold in thresholds:
        df_f1_score_data = get_f1_score_data(distance_paths, threshold, config)
        df_f1_score_data.to_pickle(result_dir + 'df_f1_{}.pkl'.format(threshold))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    get_data_to_plot(config)

