import os
import pickle
import numpy as np


def zero_pad_nr(frame_nr, len_number=6):
    len_frame_nr = len(str(frame_nr))
    len_padding = len_number - len_frame_nr
    new_nr = ('0'*len_padding) + str(frame_nr)
    return new_nr

def return_VM_path(movie_name, frame_nr):
    fn = zero_pad_nr(frame_nr)
    path = 'emma@40.68.75.18:/movie-drive/frames/{}/frame_{}.jpg'.format(movie_name, fn)
    return path

def init_frame_nrs():
    fns = range(0, 800000)
    fns = [zero_pad_nr(f) for f in fns]
    fns = fns[::25]
    fns = fns[60:-300]
    return np.array(fns)


def get_paths_incorrect_frames(incorrect_matches, hash_type):
    frame_nrs = init_frame_nrs()
    all_v_paths = []
    all_t_paths = []
    for movie_name in incorrect_matches[hash_type].keys():
        video_indeces, trailer_indeces = incorrect_matches[hash_type][movie_name]
        t_indeces = list(set(trailer_indeces))
        v_indeces = list(set(video_indeces))
        t_fns = frame_nrs[t_indeces]
        v_fns = frame_nrs[v_indeces]
        t_paths = [return_VM_path(movie_name, fn) for fn in t_fns]
        v_paths = [return_VM_path(movie_name, fn) for fn in v_fns]

        all_t_paths += t_paths
        all_v_paths += v_paths

    return all_t_paths, all_v_paths


def download_incorrect_frames(incorrect_matches):
    hash_types = incorrect_matches.keys()

    for hash_type in hash_types:

        v_paths, t_paths = get_paths_incorrect_frames(hash_type)
        wrong_frames_path = '/home/emsala/movie-drive/results/wrong_frames/{}/'.format(hash_type)

        try:
            os.mkdir(wrong_frames_path)
            os.chdir(wrong_frames_path)
        except:
            os.chdir(wrong_frames_path)

        for t_path in t_paths:

            movie_name = t_path.split('/')[-2]
            new_name = movie_name + '_trailer_' + t_path.split('/')[-1]

            command = 'scp {} {}{}'.format(t_path, wrong_frames_path, new_name)
            print(command)
            os.system(command)

        for v_path in v_paths:
            movie_name = v_path.split('/')[-2]
            new_name = movie_name + '_movie_' + v_path.split('/')[-1]

            command = 'scp {} {}{}'.format(v_path, wrong_frames_path, new_name)
            print(command)
            os.system(command)


if __name__ == "__main__":

    with open('incorrect_matches.pickle', 'rb') as handle:
        im = pickle.load(handle)

    download_incorrect_frames(im)