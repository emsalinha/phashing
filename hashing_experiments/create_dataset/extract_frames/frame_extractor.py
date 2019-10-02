import cv2
import os
from zero_pad_nr import zero_pad_nr
import time
# from create_dataset.extract_frames.zero_pad_nr import zero_pad_nr
import typing
import glob
import os
import time
import argparse
from extract_frames import extract
import csv
from typing import List

# TODO: class van maken, zodat importeren makkelijk is van een losse functionaliteit vanuit andere omgeving

# TODO: replace try except with if not os.path.exists()

# TODO: geen aparte files for enkele functies, alleen groepen functies

# TODO: utils folder voor de vaakgebruikte functies (utils/frame) etc., hoogte hangt af van waar het door gebruikt wordt

class FrameExtractor:

	def __init__(self, movie_paths: List, frames_dir: str, fps=25, output_path=None, print=True):
		self.movie_paths = movie_paths
		self.frames_dir = frames_dir
		self.fps = fps
		self.output_path = output_path
		self.print = print
		if self.output_path == None:
			self.save = False
		else:
			self.save = True



	def extract_frames(self, config):

		n_extracted_movies = len(glob.glob(self.frames_dir + '/*'))
		n_movies = len(self.movie_paths)
		n_movies_to_extract = n_movies - n_extracted_movies

		if self.save:
			speed = {}
			output_file_path = os.path.join(output_path, 'speed_extracting.csv')
			results = csv.writer(open(output_file_path, 'w'))

		for i in range(0, len(movie_paths)):

			movie_path = movie_paths[i]

			movie_name = os.path.basename(movie_path).split('.')[0]
			frames_path = os.path.join(self.frames_dir, movie_name)

			try:
				os.mkdir(frames_path)
			except:
				msg = 'Can not make frame folder. Assume already exists and skip extracting movie {}'.format(movie_name)
				print(msg)

			if self.print:
				msg = 'extract {}, {} of {} movies'.format(movie_path, i, n_movies_to_extract)
				print(msg)

			start = time.time()

			n_frames = self.extract(movie_path, frames_path, 6)

			end = time.time()

			duration = (end - start)
			print('{} frames in {} time'.format(n_frames, duration))

			speed[duration] = n_frames
			for key, val in speed.items():
				results.writerow([key, val])



	def get_frame_rate(self, vidcap):

		(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

		if int(major_ver) < 3:
			frames_per_second = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
		else:
			frames_per_second = vidcap.get(cv2.CAP_PROP_FPS)

		return frames_per_second

	def extract(self, movie_path, write_path='', len_number=6):

		vidcap = cv2.VideoCapture(movie_path)

		fps_movie = self.get_frame_rate(vidcap)
		sample_rate = int(self.fps_movie/fps_movie)

		success,image = vidcap.read()
		count = 0
		start = time.time()


		while success:

			if (count%10000 == 0) and (count != 0):
				duration = (time.time() - start)
				print(duration/count)

			if count % sample_rate == 0:
				success,image = vidcap.read()
				n = zero_pad_nr(count, len_number)
				frame_path = write_path + 'frame_{}.jpg'.format(n)
				cv2.imwrite(frame_path, image)  # save frame as JPEG file

			count += 1

		#last_corrupted_frame = frame_path
		#os.remove(last_corrupted_frame)

		return count



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=True, help='Running on VM or not')
	# TODO: path als argument
	# TODO: optional output file path for saving, anders printen in console
	config = parser.parse_args()
	extract_frames(config)

	if config.VM:
		home = '/'
	else:
		home = os.getenv('HOME') + '/'

	drive_path = home + 'movie-drive/'
	movie_paths = sorted(glob.glob(drive_path + 'movies/*'))
	frame_paths = glob.glob(drive_path + 'frames/*')

	output_path = drive_path + 'results/'