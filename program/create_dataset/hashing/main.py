import glob
import os
import csv
import argparse
from create_dataset.hashing.hash_and_write import hash_and_write
from create_dataset.hashing.hash_functions import DCT_hash, AVG_hash


def main_hash_and_write(config):


	if config.VM:
		home = '/movie-drive/'
	else:
		home = os.getenv('HOME') + '/movie-drive/'

	speed = {}
	results = csv.writer(open(home + 'results/speed_hashing.csv', 'w'))

	frame_dirs = glob.glob(home + 'frames/*')


	hash_params = {
		'augmentation': False,
		'hash_size': None,
		'high_freq_factor': 8,
		'vertical': 0,
		'horizontal': 0
	}

	hash_methods = [DCT_hash, AVG_hash]
	hash_sizes = [4, 8, 12]

	for frame_dir in frame_dirs:

		frame_paths = glob.glob(frame_dir + '/*')
		movie_name = frame_paths[0].split('/')[-2]
		hashes_wd = home + 'hashes/' + movie_name

		try:
			os.chdir(hashes_wd)
		except:
			os.mkdir(hashes_wd)
			os.chdir(hashes_wd)

		for hash_method in hash_methods:
			for hash_size in hash_sizes:

				hash_params['hash_size'] = hash_size
				speed_per_hash = hash_and_write(movie_name, frame_paths, hash_method, hash_params)

				hash_name = '{}_{}'.format(hash_method.__name__, hash_size)
				if hash_name in speed:
					speed[hash_name].append(speed_per_hash)
				else:
					speed[hash_name] = [speed_per_hash]
				for key, val in speed.items():
					results.writerow([key, val])



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
	config = parser.parse_args()
	main_hash_and_write(config)
