import cv2
import os
from zero_pad_nr import zero_pad_nr
import time

def extract(movie_path, write_path='', len_number=6):
	vidcap = cv2.VideoCapture(movie_path)
	success,image = vidcap.read()
	count = 0
	start = time.time()

	while success:
		#vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
		if (count%10000 == 0) and (count != 0):
			duration = (time.time() - start)
			print(duration/count)
		success,image = vidcap.read()
		n = zero_pad_nr(count, len_number)
		frame_path = write_path + 'frame_{}.jpg'.format(n)
		cv2.imwrite(frame_path, image)  # save frame as JPEG file
		count += 1

	last_corrupted_frame = frame_path
	os.remove(last_corrupted_frame)

	return count


