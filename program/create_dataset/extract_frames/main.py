import glob
import os
import time
import argparse
from extract_frames import extract
import csv


def extract_frames(config):

	if config.VM:
		home = '/'
	else:
		home = os.getenv('HOME') + '/'


	drive_path = home + 'movie-drive/'
	movie_paths = sorted(glob.glob(drive_path + 'movies/*'))
	frame_paths = glob.glob(drive_path + 'frames/*')
	N = len(movie_paths) - len(frame_paths)
	speed = {}
	results = csv.writer(open(drive_path + 'results/speed_extracting.csv', 'w'))
        
	for movie_path in movie_paths:
		start = time.time()
		print(movie_path, ' {} of {} movies'.format(movie_paths.index(movie_path), N))

		movie_name = movie_path.split('/')[-1].split('.')[0]
		frames_path = drive_path + 'frames/' + movie_name + '/'
		try:
			os.mkdir(frames_path)
		except:
			continue

		n_frames = extract(movie_path, frames_path, 6)

		end = time.time()

		duration = (end - start)
		print('{} frames in {} time'.format(n_frames, duration))
		
		speed[duration] = n_frames
		for key, val in speed.items():
			results.writerow([key, val])

	results.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=True, help='Running on VM or not')
	config = parser.parse_args()
	extract_frames(config)
