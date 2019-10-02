import os
import pandas as pd
import typing
from phashing.utils.pickle.functions import open_pickle
from phashing.create_dataset.inspect_matches.matching_frames_downloader import MatchingFramesDownloader

class Annotator:
    """
    input is matches and output is annotated dataset
    """

    def __init__(self, matches):
        self.matching_frames_getter = MatchingFramesDownloader(matches)
        self.annotated_dataset = pd.DataFrame()

    def annotate(self):

        frame_nr = []
        movie = []

        for movie_name, df_matches in self.matching_frames_getter.get_matching_frames():
            frame_nrs = sorted(df_matches.movie_fns.unique())
            movies = [movie_name] * len(frame_nrs)

            frame_nr += frame_nrs
            movie += movies

        self.annotated_dataset['movie'] = movie
        self.annotated_dataset['frame_nr'] = frame_nr




if __name__ == '__main__':

    matches_path = '/movie-drive/results/matches/rb/matches_035.pickle'
    matches = open_pickle(matches_path)

    annotator = Annotator(matches)
    annotator.annotate()
    print(annotator.annotated_dataset)
