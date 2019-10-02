import h5py
import numpy as np
import pandas as pd
import argparse
import glob
# from sklearn.metrics import f1_score as calc_f1
# from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import confusion_matrix
import os
#TODO: take maximum of predictions per frame or all predictions above the threshold?
#TODO: check for every threshold or pick one threshold? if so what thresholds ("no cherry picking") thresholds = range(0,1,0.1)

def get_f1_score_data(paths, threshold, config):

    df_original = pd.DataFrame()
    for path in paths:
        df = f1_score_data(path, threshold, config)
        df_original = pd.concat([df_original, df])

    return df_original

def f1_score_data(distances_path, threshold, config):
    """
    calculate fp, fn, tp, tn per movie per hashtype for a certain threshold
    :param distances_path: path to hdf5 file with distances
    :param threshold: upper boundary for distance for similar frames (below is similar)
    :return: pandas dataframe: {moviename, hashtype, fp, fn, tp, tn}
    """

    if config.VM:
        from utils.traverse_datasets import traverse_datasets
    else:
        from get_data.extract_data.utils.traverse_datasets import traverse_datasets

    n_frames_trailer = config.trailer_length * 60

    movie_name = distances_path.split('/')[-2]
    distances_store = h5py.File(distances_path, 'a')
    datasets = [d for d in traverse_datasets(distances_path)]
    f1_score_df = pd.DataFrame()
    tns = []
    fps = []
    fns = []
    tps = []

    for dataset in datasets:
        distances = distances_store[dataset][:]
        distances = np.amin(distances, axis=1)
        y_pred = get_y_pred(distances, threshold)
        y_true = get_y_true(distances, n_frames_trailer)
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        tns.append(tn)
        fps.append(fp)
        fns.append(fn)
        tps.append(tp)

    movie_names = [movie_name] * len(datasets)
    f1_score_df['movie_name'] = movie_names
    f1_score_df['hash_type'] = datasets
    f1_score_df['tn'] = tns
    f1_score_df['fp'] = fps
    f1_score_df['fn'] = fns
    f1_score_df['tp'] = tps

    return f1_score_df


def get_y_pred(distances, threshold):
    y_pred = [1 if distance < threshold else 0 for distance in distances]
    y_pred = np.array(y_pred)
    return y_pred


def get_y_true(distances, len_trailer):
    n_frames = distances.shape[0]
    y_true = [0] * 60 + [1] * len_trailer + [0] * (n_frames-len_trailer-60)
    y_true = np.array(y_true)
    return y_true

def get_f1_score(cm):
    tn, fp, fn, tp = cm.ravel()
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * ((precision * recall)/(precision+recall))
    return f1_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    parser.add_argument('--trailer_length', type=int, default=5, help='trailer length in minutes')
    config = parser.parse_args()
    home = os.getenv('HOME') + '/movie-drive/'
    result_dir = home + 'results/'
    df_f1_dir = result_dir + 'f1_scores/'
    distance_dirs = sorted(glob.glob(home + 'distances/*'))
    distances_paths = [sorted(glob.glob(distance_dir + '/*'))[0] for distance_dir in distance_dirs]

    thresholds = np.arange(0, 1, 0.025)
    for threshold in thresholds:
        df_f1_score_data = get_f1_score_data(distances_paths, threshold, config)
        df_f1_score_data.to_pickle(df_f1_dir + 'df_f1_{}.pkl'.format(threshold))


    #write_hists_occurences(result_dir, distances_paths, config)


