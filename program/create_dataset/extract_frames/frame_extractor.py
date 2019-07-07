import argparse
import csv
import glob
import os
import time
from typing import List
from PIL import Image
import numpy as np




import cv2
from math import ceil


class FrameExtractor:

	def __init__(self, movie_paths: List, frames_dir: str, fps=25, output_path=None, print=True, skip_black_frames=False):
		self.movie_paths = movie_paths
		self.frames_dir = frames_dir
		self.fps = fps
		self.output_path = output_path
		self.print = print
		self.speed = {}
		self.skip_black_frames = skip_black_frames
		if self.output_path == None:
			self.save = False
		else:
			self.save = True


	def extract_frames_movies(self):

		n_extracted_movies = len(glob.glob(self.frames_dir + '/*'))
		n_movies = len(self.movie_paths)
		n_movies_to_extract = n_movies - n_extracted_movies

		if self.save:
			output_file_path = os.path.join(output_path, 'speed_extracting.csv')
			results = csv.writer(open(output_file_path, 'w'))

		for i in range(0, len(movie_paths)):

			movie_path = movie_paths[i]

			movie_name = os.path.basename(movie_path).split('.')[0]
			frames_path = os.path.join(self.frames_dir, movie_name)


			if os.path.exists(frame_paths):
				msg = 'Frame folder exists -> skip extracting movie {}'.format(movie_name)
				print(msg)
				continue
			else:
				os.mkdir(frames_path)

			if self.print:
				msg = 'extract {}, {} of {} movies'.format(movie_path, i, n_movies_to_extract)
				print(msg)

			n_frames_movie, duration_movie = self.extract_frames_movie(movie_path, frames_path)

			if self.print:
				msg = '{} frames in {} time'.format(n_frames_movie, duration_movie)
				print(msg)

			if self.save:
				results.writerow([movie_name, duration_movie, n_frames_movie])


	def extract_frames_movie(self, movie_path, frames_path):

		vidcap = cv2.VideoCapture(movie_path)
		fps_movie, n_frames = self.get_frame_info(vidcap)

		sample_rate = ceil(self.fps/fps_movie)

		n_frames /= sample_rate
		len_frame_numbers = len(str(n_frames))

		success, image = vidcap.read()
		count = 0
		start = time.time()

		while success:

			if (count%10000 == 0) and (count != 0):
				duration = (time.time() - start)
				print(duration/count)

			if count % sample_rate == 0:
				success,image = vidcap.read()

				if self.skip_black_frames:
					black = self.black_frame(image)
					if black:
						continue
					else:
						pass

				n = self.zero_pad_nr(count, len_frame_numbers)
				frame_path = os.path.join(frames_path + 'frame_{}.jpg'.format(n))
				cv2.imwrite(frame_path, image)  # save frame as JPEG file

			count += 1

		end = time.time()
		duration = end-start

		last_corrupted_frame = frame_path
		os.remove(last_corrupted_frame)

		return n_frames, duration

	def zero_pad_nr(self, frame_nr, len_number):
		len_frame_nr = len(str(frame_nr))
		len_padding = len_number - len_frame_nr
		new_nr = ('0'*len_padding) + str(frame_nr)
		return new_nr

	def get_frame_info(self, vidcap):
		(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
		if int(major_ver) < 3:
			frames_per_second = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
			length = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
		else:
			frames_per_second = vidcap.get(cv2.CAP_PROP_FPS)
			length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

		return frames_per_second, length

	def black_frame(self, img):
		img = np.asarray(img)
		black = np.all(img == 0)
		return black

	def change_movie_paths(self, movie_paths: List):
		self.movie_paths = movie_paths

	def change_frames_dir(self, frames_dir: str):
		self.frames_dir = frames_dir

	def change_output_path(self, output_path: str):
		self.output_path = output_path
		if self.output_path == None:
			self.save = False
		else:
			self.save = True

	def change_fps(self, fps: int):
		self.fps = fps

	def change_print(self, print: bool):
		self.print = print


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=True, help='Running on VM or not')
	parser.add_argument('--movie_paths', type=str, default=None, help='location of movies')
	parser.add_argument('--frames_dir', type=str, default=None, help='location to save frames')
	parser.add_argument('--fps', type=int, default=25, help='sample rate in frames per second')
	parser.add_argument('--output_path', type=str, default=None, help='saving speed file')
	parser.add_argument('--print', type=bool, default=True, help='whether or not to print debugging messages')

	config = parser.parse_args()

	if config.VM:
		home = '/'
	else:
		home = os.getenv('HOME') + '/'

	drive_path = home + 'movie-drive'
	frames_dir = home + 'movie-drive/frames'
	movie_paths = sorted(glob.glob(drive_path + 'movies/*'))
	frame_paths = glob.glob(drive_path + 'frames/*')

	output_path = drive_path + 'results/'

	frame_extractor = FrameExtractor(movie_paths=movie_paths, frames_dir=frames_dir)
	frame_extractor.extract_frames_movies()




