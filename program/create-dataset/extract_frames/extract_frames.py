import cv2


def extract_frames(movie_path):
	vidcap = cv2.VideoCapture(movie_path)
	success,image = vidcap.read()
	count = 0
	while success:
		#vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
		success,image = vidcap.read()
		n = zero_pad_nr(count, len_number=6)
		cv2.imwrite('frame_{}.jpg'.format(n), image)  # save frame as JPEG file
		count += 1