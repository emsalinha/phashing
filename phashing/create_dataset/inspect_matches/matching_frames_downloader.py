import os
import pickle
import numpy as np
import pandas as pd
import glob

class MatchingFramesDownloader:
    def __init__(self, matches_path, download_dir):
        self.matches = self.__open__(matches_path)
        self.threshold = self.__get_threshold__(matches_path)

        self.download_dir = self.__create_dir__(download_dir)

        self.paths_matching_frames = []

        self.max_matches_per_video = 50


    def set_download_dir(self, download_dir):
        self.download_dir = self.__create_dir__(download_dir)

    def set_matches_path(self, matches_path):
        self.matches = self.__open__(matches_path)
        self.threshold = self.__get_threshold__(matches_path)

    def __create_dir__(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def __open__(self, path):
        with open(path, 'rb') as handle:
            return pickle.load(handle)

    def __get_threshold__(self, path):
        threshold = path.split('_')[-1].split('.')[0]
        threshold = threshold[0] + '.' + threshold[1:]
        return float(threshold)

    def download_matching_frames(self):

        for movie_name, matches in self.matches.items():
            if movie_name.startswith('00'):
                continue

            if matches['distances'].size < 1:
                pass

            df_matches = self.__create_dataframe__(matches)
            #df_matches = self.__reduce_match_amount__(df_matches)
            df_matches = self.__group_minimum_distances__(df_matches)

            df_matches = df_matches[df_matches['trailer_fns'] != 0].reset_index()

            df_matches['v_path'] = df_matches['movie_fns'].apply(lambda x: self.return_VM_path(movie_name, int(x)))
            df_matches['t_path'] = df_matches['trailer_fns'].apply(lambda x: self.return_VM_path(movie_name, int(x)))

            self.__download__(df_matches)

    def __filter_group__(self, dfg, col):
        return dfg[dfg[col] == dfg[col].min()]

    def __group_minimum_distances__(self, df):
        return df.groupby('trailer_fns', group_keys=False).apply(lambda x: self.__filter_group__(x, 'distances'))

    def __download__(self, df_matches):

        for i, row in df_matches.iterrows():
            distance, v_path, t_path = row['distances'], row['v_path'], row['t_path']

            command = self.__create_command__(i, t_path, distance, subset='trailer')
            print(command)
            os.system(command)

            command = self.__create_command__(i, v_path, distance, subset='movie')
            print(command)
            os.system(command)


    def __create_command__(self, i, frame_path, distance, subset):
        distance = str(round(distance,2)).replace('.', '')

        f_name = frame_path.split('/')[-1].split('.')[0]
        f_ext = frame_path.split('/')[-1].split('.')[1]
        movie_name = frame_path.split('/')[-2]
        new_name = movie_name + '_{}_{}_{}'.format(i, subset, f_name) + '_dist_{}'.format(distance) + '.' + f_ext
        to_path = os.path.join(self.download_dir, new_name)
        command = 'scp {} {}'.format(frame_path, to_path)
        return command


    def __create_dataframe__(self, matches):
        matches['movie_fns'] = [v.item() for v in matches['movie_fns']]
        matches['trailer_fns'] = [t.item() for t in matches['trailer_fns']]


        data = {
            'distances': matches['distances'],
            'movie_fns': matches['movie_fns'],
            'trailer_fns': matches['trailer_fns']
        }
        df_matches = pd.DataFrame.from_dict(data)
        return df_matches

    def __reduce_match_amount__(self, df_matches):
        df_matches = df_matches.sort_values(by='distances', ascending=False).reset_index()
        r, c = df_matches.shape
        max_row = min(r, self.max_matches_per_video)
        df_matches = df_matches.iloc[:max_row, :]
        return df_matches

    def get_unique_unlinked_paths(self, movie_name, subset_im):
        movie_fns, trailer_fns, distances = subset_im
        movie_fns = sorted(list(set([v.item() for v in movie_fns])))
        trailer_fns = sorted(list(set([t.item() for t in trailer_fns])))

        v_paths = [self.return_VM_path(movie_name, fn) for fn in movie_fns]
        t_paths = [self.return_VM_path(movie_name, fn) for fn in trailer_fns]
        return v_paths, t_paths


    def zero_pad_nr(self, frame_nr, len_number=6):
        len_frame_nr = len(str(frame_nr))
        len_padding = len_number - len_frame_nr
        new_nr = ('0'*len_padding) + str(frame_nr)
        return new_nr

    def return_VM_path(self, movie_name, frame_nr):
        fn = self.zero_pad_nr(frame_nr)
        path = 'emma@40.68.75.18:/movie-drive/frames/{}/frame_{}.jpg'.format(movie_name, fn)
        return path

    # def init_frame_nrs(self):
    #     fns = range(0, 8000000)
    #     fns = [self.zero_pad_nr(f) for f in fns]
    #     fns = fns[::25]
    #     fns = fns[60:-300]
    #     return np.array(fns)



if __name__ == "__main__":

    home = os.getenv('HOME')
    dir = os.path.join(home, 'movie-drive/results/matches/rb')
    d_dir = ('/home/emsala/movie-drive/results/matches/images')
    matches_paths = sorted(glob.glob(dir + '/*'))
    #matches_paths = [matches_paths[-2]]
    #for matches_path in matches_paths:
    frame_downloader = MatchingFramesDownloader('/home/emsala/movie-drive/results/matches/rb/matches_04.pickle', download_dir=d_dir)
    # new_folder = os.path.join(d_dir, str(frame_downloader.threshold).replace('.', ''))
    # frame_downloader.set_download_dir(new_folder)
    frame_downloader.download_matching_frames()