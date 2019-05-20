import argparse
import os
import glob
import numpy as np
import h5py


def get_data_to_plot(config):

    if config.VM:
        home = '/movie-drive/'
        from min_max import get_min_max
        from f1_score_data import get_f1_score_data
        from hist_occurences import write_hists_occurences
        from significance import get_significances
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from plotting.get_data.min_max import get_min_max
        from plotting.get_data.f1_score_data import get_f1_score_data
        from plotting.get_data.hist_occurences import write_hists_occurences
        from plotting.get_data.significance import get_significances

    distance_dirs = sorted(glob.glob(home + 'distances/*'))
    distances_paths = [glob.glob(distance_dir + '/*')[0] for distance_dir in distance_dirs]
    distances_all_movies = [dp for dp in distances_paths if 'all_movies' in dp][0]
    distances_paths = [dp for dp in distances_paths if 'all_movies' not in dp]

    result_dir = home + 'results/'

    df_min_max = get_min_max(distances_paths, config)
    df_min_max.to_pickle(result_dir + 'df_min_max.pkl')

    thresholds = np.arange(0, 1, 0.1)
    for threshold in thresholds:
        df_f1_score_data = get_f1_score_data(distances_paths, threshold, config)
        df_f1_score_data.to_pickle(result_dir + 'df_f1_{}.pkl'.format(threshold))

    hist_dir = result_dir + 'histograms/'
    write_hists_occurences(hist_dir, distances_paths, config)

    df_bonferroni, df_anova = get_significances(distances_all_movies, config)
    df_bonferroni.to_pickle(result_dir + 'bonferroni_results.pkl')
    df_anova.to_pickle(result_dir + 'anova_results.pkl')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    get_data_to_plot(config)

