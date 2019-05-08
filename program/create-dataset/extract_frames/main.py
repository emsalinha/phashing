import glob
import os
import time

from

start = time.time()

if 'VM':
	home = '/'
else:
	home = os.getenv('HOME') + '/'

drive_path = home + 'movie-drive/'

movie_paths = glob.glob(drive_path + 'movies/*')

for movie_path in movie_paths:
	movie_name = movie_path.split('/')[-1].split('.')[0]
	frames_path = drive_path + 'frames/' + movie_name
	os.mkdir(frames_path)




#implement to remove last frame!!! cause its not completely loaded or whatever
