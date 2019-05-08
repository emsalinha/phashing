import glob
import os
import time
import argparse
from create_dataset.extract_frames.extract_frames import extract
import csv


def extract_frames(config):

	if config.VM:
		home = '/'
	else:
		home = os.getenv('HOME') + '/'


	drive_path = home + 'movie-drive/'
	movie_paths = glob.glob(drive_path + 'movies/*')

	results = csv.writer(open(drive_path + 'results/speed_extracting.csv', 'w'))
	speed = {}

	for movie_path in movie_paths:
		start = time.time()

		movie_name = movie_path.split('/')[-1].split('.')[0]
		frames_path = drive_path + 'frames/' + movie_name + '/'
		try:
			os.mkdir(frames_path)
		except:
			pass

		n_frames = extract(movie_path, frames_path, 6)

		end = time.time()

		duration = (end - start)
		speed[duration] = n_frames
		for key, val in speed.items():
			results.writerow([key, val])

	results.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
	config = parser.parse_args()
	extract_frames(config)
