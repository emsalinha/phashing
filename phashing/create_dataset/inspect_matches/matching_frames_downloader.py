import os
from phashing.utils.pickle.functions import open_pickle
from phashing.utils.frames.zero_pad_nr import zero_pad_nr
import numpy as np
import pandas as pd
import glob
import sys

class MatchingFramesDownloader:

    def __init__(self, matches_path, download_dir):
        self.matches = open_pickle(matches_path)
        self.threshold = self.__get_threshold__(matches_path)

        self.from_address = 'emma@40.68.75.18:'
        self.to_address = 'emsala@185.127.108.13:'

        self.download_dir = download_dir

        self.max_matches_per_video = 50

    def set_download_dir(self, download_dir):
        self.download_dir = download_dir

    def set_matches_path(self, matches_path):
        self.matches = open_pickle(matches_path)
        self.threshold = self.__get_threshold__(matches_path)

    def __create_dir__(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir

    def __return_VM_path__(self, movie_name, frame_nr):
        fn = zero_pad_nr(frame_nr)
        path = '/movie-drive/frames/{}/frame_{}.jpg'.format(movie_name, fn)
        return path

    def download_matching_frames(self):

        for movie_name, matches in self.matches.items():

            print('downloading {}'.format(movie_name))

            if matches['distances'].size < 1:
                continue

            df_matches = self.__create_dataframe__(matches)
            #df_matches = self.__reduce_match_amount__(df_matches)
            df_matches = self.__group_minimum_distances__(df_matches)

            #remove first frame because generally black
            df_matches = df_matches[df_matches.trailer_fns != 0]
            df_matches = df_matches.reset_index()

            #self.__download_matching_pairs__(df_matches, movie_name)
            self.__download_video_matches__(df_matches, movie_name)


    def __filter_group__(self, df, col):
        return df[df[col] == df[col].min()]

    def __group_minimum_distances__(self, df):
        #create groupes per trailer_fn, then filters these groups and gets only distances within group with minimum value
        df_grouped = df.groupby('trailer_fns', group_keys=False).apply(lambda x: self.__filter_group__(x, 'distances'))
        return df_grouped

    def __download_video_matches__(self, df_matches, movie_name):
        movie_matches = sorted(df_matches.movie_fns.unique())
        paths = [self.__return_VM_path__(movie_name, int(x)) for x in movie_matches]
        for path in paths:
            from_path = self.__get_from_path__(path)
            to_path = self.__create_to_path__(frame_path=path, frame_type='movie')
            self.__execute_command__(from_path, to_path)


    def __download_matching_pairs__(self, df_matches, movie_name):
        df_matches['v_path'] = df_matches['movie_fns'].apply(lambda x: self.__return_VM_path__(movie_name, int(x)))
        df_matches['t_path'] = df_matches['trailer_fns'].apply(lambda x: self.__return_VM_path__(movie_name, int(x)))

        for i, row in df_matches.iterrows():
            if i == 0 or i % 10 == 0:
                print('downloading matches {} of {}'.format(i, len(df_matches)))
            distance, v_path, t_path = row['distances'], row['v_path'], row['t_path']

            to_path = self.__create_to_path__(frame_path=t_path, frame_type='trailer', distance=distance, i=i)
            from_path = self.__get_from_path__(t_path)

            self.__execute_command__(from_path, to_path)

            to_path = self.__create_to_path__(frame_path=v_path, frame_type='movie', distance=distance, i=i)
            from_path = self.__get_from_path__(v_path)

            self.__execute_command__(from_path, to_path)


    def __execute_command__(self, from_path, to_path):

            command = 'scp {} {}'.format(from_path, to_path)
            #print(command)
            os.system(command)


    def __create_to_path__(self, frame_path, frame_type, distance=None, i=''):

        base_name = frame_path.split('/')[-1].split('.')[0]
        ext = frame_path.split('/')[-1].split('.')[1]
        movie_name = frame_path.split('/')[-2]

        new_base_name =  '{}_{}_{}_{}'.format(movie_name, i, frame_type, base_name)

        if distance is not None:
            distance = str(round(distance, 2)).replace('.', '')
            new_base_name = new_base_name + '_dist_{}'.format(distance)

        new_name = new_base_name + '.' + ext

        to_path = os.path.join(self.download_dir, new_name)

        return to_path

    def __get_from_path__(self, path):
        from_path = self.from_address + path
        return from_path

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


    # def init_frame_nrs(self):
    #     fns = range(0, 8000000)
    #     fns = [zero_pad_nr(f) for f in fns]
    #     fns = fns[::25]
    #     fns = fns[60:-300]
    #     return np.array(fns)


    def __get_threshold__(self, path):
        threshold = path.split('_')[-1].split('.')[0]
        threshold = threshold[0] + '.' + threshold[1:]
        return float(threshold)

if __name__ == "__main__":

    dir = '/home/emsala/movie-drive/results/matches/rb'
    matches_paths = sorted(glob.glob(dir + '/*'))

    d_dir = '/home/emsala/movie-drive/results/matches/images_035'

    #matches_paths = [matches_paths[-2]]
    #for matches_path in matches_paths:
    matches_path = os.path.join(dir, 'matches_035.pickle')
    frame_downloader = MatchingFramesDownloader(matches_path, download_dir=d_dir)
    #print(frame_downloader.download_dir)
    # new_folder = os.path.join(d_dir, str(frame_downloader.threshold).replace('.', ''))
    # frame_downloader.set_download_dir(new_folder)
    frame_downloader.download_matching_frames()