import glob
import os

import cv2

wd = '/home/emsala/Documenten/Studie/These/dataset-maken/dataset/trailers'

trailer = 'trailer_1'

trailer_wd = wd + '/' + trailer + '/' + 'trailer'
frames_wd = wd + '/' + trailer + '/' + 'frames'


trailers = glob.glob(trailer_wd + '/*')
trailers = [trailer.split('/')[-1] for trailer in trailers if trailer.endswith('.py') == False]

for trailer in trailers:
	trailer_name = trailer[0:6]
	os.chdir(trailer_wd)
	vidcap = cv2.VideoCapture(trailer)
	os.chdir(frames_wd)
	os.mkdir('{}-frames'.format(trailer_name))
	os.chdir(frames_wd + '/' + '{}-frames'.format(trailer_name))
	#vidcap.set(cv2.CAP_PROP_POS_MSEC,20000)

	success,image = vidcap.read()
	count = 0
	while success:
	    #vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
	    success,image = vidcap.read()
	    cv2.imwrite("{}-frame-{}.jpg".format(trailer_name, count), image)   # save frame as JPEG file
	    count += 1

#implement removal of last trailer