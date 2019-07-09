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

	def __init__(self, video_paths: List, frames_dir: str, fps=1, output_path=None, print=True, skip_black_frames=False):
		self.video_paths = video_paths
		self.frames_dir = frames_dir
		self.fps = fps
		self.output_path = output_path
		self.print = print
		self.speed = {}
		self.skip_black_frames = skip_black_frames
		self.frames_path = str()
		if self.output_path == None:
			self.save = False
		else:
			self.save = True

	def extract_frames_videos(self):

		n_extracted_videos = len(glob.glob(self.frames_dir + '/*'))
		n_videos = len(self.video_paths)
		n_videos_to_extract = n_videos - n_extracted_videos

		if self.save:
			output_file_path = os.path.join(output_path, 'speed_extracting.csv')
			results = csv.writer(open(output_file_path, 'w'))

		for i in range(0, len(video_paths)):

			video_path = video_paths[i]

			video_name = os.path.basename(video_path).split('.')[0]
			self.frames_path = os.path.join(self.frames_dir, video_name)


			if os.path.exists(self.frames_path):
				msg = 'Frame folder exists -> skip extracting video {}'.format(video_name)
				print(msg)
				continue
			else:
				os.mkdir(self.frames_path)

			if self.print:
				msg = 'extract {}, {} of {} videos'.format(video_path, i, n_videos_to_extract)
				print(msg)

			n_frames_video, duration_video = self.extract_frames_video(video_path)

			if self.print:
				msg = '{} frames in {} time'.format(n_frames_video, duration_video)
				print(msg)

			if self.save:
				results.writerow([video_name, duration_video, n_frames_video])


	def extract_frames_video(self, video_path):

		vidcap = cv2.VideoCapture(video_path)
		fps_video, n_frames = self.get_frame_info(vidcap)

		sample_rate = ceil(fps_video/self.fps)

		n_frames = int(n_frames/sample_rate)
		len_frame_numbers = max(len(str(n_frames)), 6)

		success, image = vidcap.read()
		count = 0
		start = time.time()

		n_frame = 0

		while success:
			success, image = vidcap.read()

			if (count%10000 == 0) and (count != 0):
				duration = (time.time() - start)
				print(duration/count)

			if count % sample_rate == 0:

				if self.skip_black_frames:
					black = self.black_frame(image)
					if black:
						continue
					else:
						pass

				n = self.zero_pad_nr(n_frame, len_frame_numbers)
				frame_path = os.path.join(self.frames_path, 'frame_{}.jpg'.format(n))
				cv2.imwrite(frame_path, image)  # save frame as JPEG file
				n_frame += 1

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

	def change_video_paths(self, video_paths: List):
		self.video_paths = video_paths

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
	parser.add_argument('--video_paths', type=str, default=None, help='location of videos')
	parser.add_argument('--frames_dir', type=str, default=None, help='location to save frames')
	parser.add_argument('--fps', type=int, default=1, help='sample rate in frames per second')
	parser.add_argument('--output_path', type=str, default=None, help='saving speed file')
	parser.add_argument('--print', type=bool, default=True, help='whether or not to print debugging messages')

	config = parser.parse_args()

	if config.VM:
		home = '/'
	else:
		home = os.getenv('HOME') + '/'

	drive_path = home + 'movie-drive/'
	frames_dir = home + 'movie-drive/trailer_frames/'
	try:
		os.mkdir(frames_dir)
	except:
		'folder exists'
	video_paths = sorted(glob.glob(drive_path + 'trailers/*'))
	frame_paths = glob.glob(drive_path + 'frames/*')
	output_path = drive_path + 'results/trailers/'
	try:
		os.mkdir(output_path)
	except:
		'folder exists'

	frame_extractor = FrameExtractor(video_paths=video_paths, frames_dir=frames_dir, output_path=output_path)
	frame_extractor.extract_frames_videos()




