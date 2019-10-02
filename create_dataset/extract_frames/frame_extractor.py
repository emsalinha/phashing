import argparse
import csv
import glob
import os
import time
from typing import List

import cv2
import numpy as np


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

			n_frames_video, duration_video = self.extract_frames(video_path)

			if self.print:
				msg = '{} frames in {} time'.format(n_frames_video, duration_video)
				print(msg)

			if self.save:
				results.writerow([video_name, duration_video, n_frames_video])



	def extract_frames(self, video_path):

		vidcap = cv2.VideoCapture(video_path)
		fps_video, n_frames = self.__get_frame_info__(vidcap)

		success = True
		start = time.time()

		frame_n = -1

		while success:


			frame_id = int(round(vidcap.get(1)))
			# current frame number, rounded b/c sometimes you get frame intervals which aren't integers...this adds a little imprecision but is likely good enough
			success, image = vidcap.read()

			if (frame_id%10000 == 0) and (frame_id != 0):
				duration = (time.time() - start)
				print(duration/frame_id)

			if (frame_id * self.fps) % int(fps_video) == 0:

				if self.skip_black_frames:
					black = self.black_frame(image)
					if black:
						continue
					else:
						pass

				frame_n += 1
				n = self.__zero_pad_nr__(frame_n, len_number=6)
				frame_path = os.path.join(self.frames_path, 'frame_{}.jpg'.format(n))
				cv2.imwrite(frame_path, image)  # save frame as JPEG file


		end = time.time()
		duration = end-start

		last_corrupted_frame = frame_path
		os.remove(last_corrupted_frame)

		vidcap.release()

		return n_frames, duration


	def __zero_pad_nr__(self, frame_nr, len_number):
		len_frame_nr = len(str(frame_nr))
		len_padding = len_number - len_frame_nr
		new_nr = ('0'*len_padding) + str(frame_nr)
		return new_nr

	def __get_frame_info__(self, vidcap):
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

	def set_video_paths(self, video_paths: List):
		self.video_paths = video_paths

	def set_frames_dir(self, frames_dir: str):
		self.frames_dir = frames_dir

	def set_output_path(self, output_path: str):
		self.output_path = output_path
		if self.output_path == None:
			self.save = False
		else:
			self.save = True

	def set_fps(self, fps: int):
		self.fps = fps

	def set_print(self, print: bool):
		self.print = print


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--video_paths', type=str, default=None, help='location of videos')
	parser.add_argument('--frames_dir', type=str, default=None, help='location to save frames')
	parser.add_argument('--fps', type=int, default=1, help='sample rate in frames per second')
	parser.add_argument('--output_path', type=str, default=None, help='saving speed file')
	parser.add_argument('--print', type=bool, default=True, help='whether or not to print debugging messages')

	config = parser.parse_args()


	drive_path = '/movie-drive/'
	frames_dir = '/movie-drive/trailer_frames/'

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




