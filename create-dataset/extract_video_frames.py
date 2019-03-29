import cv2
import os
import glob

os.chdir('/home/emsala/Documenten/Studie/These/dataset-maken/test-hash-methode/films')
folders = glob.glob(os.getcwd() + '/*')
for folder in folders:
	if folder.startswith('film'):
		folderindex = folder.split('film-')[1]
		newfolder = 'film-' + folderindex
		os.mkdir(newfolder)
		os.chdir(os.getcwd() + '/' + newfolder)
		

vidcap = cv2.VideoCapture('SeeFood - A Fish Out Of Water (2011) Bluray Full HD 1080p Dual Audio.mkv')
#vidcap.set(cv2.CAP_PROP_POS_MSEC,20000)

success,image = vidcap.read()
count = 0
while success:
    #vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
    success,image = vidcap.read()
    cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    count += 1



#implement to remove last frame!!! cause its not completely loaded or whatever
