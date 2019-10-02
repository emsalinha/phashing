import os
import pickle
import numpy as np
import pandas as pd


class IncorrectFrameDownloader:
    def __init__(self, incorrect_matches):
        self.incorrect_matches = incorrect_matches
        self.subset_im = pd.DataFrame()
        self.hash_types = self.get_hash_types()
        self.paths_incorrect_frames = []
        #self.frame_nrs = self.init_frame_nrs()
        self.download_dir = '/home/emsala/movie-drive/results/incorrect_matches/'
        self.max_matches_per_video = 4
        self.main()


    def main(self):
        for hash_type in self.hash_types:
            for movie_name in self.incorrect_matches[hash_type].keys():
                self.get_paths_incorrect_frames(hash_type, movie_name)
                if len(self.paths_incorrect_frames) < 1:
                    continue
                else:
                    self.download_incorrect_frames(hash_type)

    def get_hash_types(self):
        hash_types = self.incorrect_matches.keys()
        hash_types = [h for h in hash_types if ('8' in h) or ('12' in h)]
        return hash_types

    def get_download_command(self, i, frame_path, distance, download_path, subset):
        distance = str(distance).replace('.', '_')[0:4]
        f_name = frame_path.split('/')[-1].split('.')[0]
        f_ext = frame_path.split('/')[-1].split('.')[1]
        movie_name = frame_path.split('/')[-2]
        new_name = movie_name + '_{}_{}_{}'.format(i, subset, f_name) + '_dist_{}'.format(distance) + '.' + f_ext
        command = 'scp {} {}{}'.format(frame_path, download_path, new_name)
        return command

    def get_paths_incorrect_frames(self, hash_type, movie_name):

        subset_im = self.incorrect_matches[hash_type][movie_name]
        self.paths_incorrect_frames = []

        if subset_im[0].size < 1:
            pass

        else:
            self.create_dataframe(subset_im)
            self.reduce_match_amount()

            for index, row in self.subset_im.iterrows():
                v, t, d = row['video_fns'], row['trailer_fns'], row['distances']
                v_path = self.return_VM_path(movie_name, int(v))
                t_path = self.return_VM_path(movie_name, int(t))
                self.paths_incorrect_frames.append((v_path, t_path, d))


    def create_dataframe(self, subset_im):
        video_fns, trailer_fns, distances = subset_im
        video_fns = [v.item() for v in video_fns]
        trailer_fns = [t.item() for t in trailer_fns]
        distances = [d.item() for d in distances]

        data = {
            'video_fns': video_fns,
            'trailer_fns': trailer_fns,
            'distances': distances
        }
        self.subset_im = pd.DataFrame.from_dict(data)

    def reduce_match_amount(self):
        self.subset_im = self.subset_im.sort_values(by='distances', ascending=True)
        r, c = self.subset_im.shape
        n_skip = int(r / self.max_matches_per_video)
        self.subset_im = self.subset_im.iloc[::n_skip, :]

    def get_unique_unlinked_paths(self, movie_name, subset_im):
        video_fns, trailer_fns, distances = subset_im
        video_fns = sorted(list(set([v.item() for v in video_fns])))
        trailer_fns = sorted(list(set([t.item() for t in trailer_fns])))

        v_paths = [self.return_VM_path(movie_name, fn) for fn in video_fns]
        t_paths = [self.return_VM_path(movie_name, fn) for fn in trailer_fns]
        return v_paths, t_paths

    def download_incorrect_frames(self, hash_type):

        download_path = self.download_dir + hash_type + '/'

        try:
            os.mkdir(download_path)
            os.chdir(download_path)
        except:
            os.chdir(download_path)

        for i in range(0, len(self.paths_incorrect_frames)):
            v_path, t_path, distance = self.paths_incorrect_frames[i]

            command = self.get_download_command(i, t_path, distance, download_path, subset='trailer')
            print(command)
            os.system(command)

            command = self.get_download_command(i, v_path, distance, download_path, subset='movie')
            print(command)
            os.system(command)


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
    im_dir = home + '/movie-drive/results/incorrect_matches/'

    with open(im_dir + 'incorrect_matches_5.pickle', 'rb') as handle:
        im = pickle.load(handle)

    frame_downloader = IncorrectFrameDownloader(im)