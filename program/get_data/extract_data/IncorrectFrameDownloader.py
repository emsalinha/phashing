import os
import pickle
import numpy as np


class IncorrectFrameDownloader:
    def __init__(self, incorrect_matches):
        self.incorrect_matches = incorrect_matches
        self.hash_types = self.get_hash_types()
        #self.frame_nrs = self.init_frame_nrs()
        self.download_dir = '/home/emsala/movie-drive/results/incorrect_matches/'
        self.main()

    def main(self):
        for hash_type in self.hash_types:
            for movie_name in self.incorrect_matches[hash_type].keys():
                v_paths, t_paths = self.get_paths_incorrect_frames(hash_type, movie_name)
                if v_paths == None:
                    continue
                else:
                    self.download_incorrect_frames(v_paths, t_paths, hash_type)

    def get_hash_types(self):
        hash_types = self.incorrect_matches.keys()
        hash_types = [h for h in hash_types if ('8' in h) or ('12' in h)]
        return hash_types

    def get_download_command(self, frame_path, download_path, subset):
        movie_name = frame_path.split('/')[-2]
        new_name = movie_name + '_{}_'.format(subset) + frame_path.split('/')[-1]
        command = 'scp {} {}{}'.format(frame_path, download_path, new_name)
        return command

    def get_paths_incorrect_frames(self, hash_type, movie_name):

        matches = self.incorrect_matches[hash_type][movie_name]

        if len(matches) < 1:
            v_paths = None
            t_paths = None

        else:
            video_fns, trailer_fns = matches

            video_fns = sorted(list(set([v.item() for v in video_fns])))
            trailer_fns = sorted(list(set([t.item() for t in trailer_fns])))

            v_paths = [self.return_VM_path(movie_name, fn) for fn in video_fns]
            t_paths = [self.return_VM_path(movie_name, fn) for fn in trailer_fns]

        return v_paths, t_paths

    def download_incorrect_frames(self, v_paths, t_paths, hash_type):

        if len(v_paths) > 20:
            v_paths = v_paths[:20]
        if len(t_paths) > 20:
            t_paths = t_paths[:20]

        download_path = self.download_dir + hash_type + '/'

        try:
            os.mkdir(download_path)
            os.chdir(download_path)
        except:
            os.chdir(download_path)

        for t_path in t_paths:
            command = self.get_download_command(t_path, download_path, subset='trailer')
            print(command)
            os.system(command)

        for v_path in v_paths:
            command = self.get_download_command(v_path, download_path, subset='movie')
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

    with open(im_dir + 'incorrect_matches_06.pickle', 'rb') as handle:
        im = pickle.load(handle)

    frame_downloader = IncorrectFrameDownloader(im)