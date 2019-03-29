import glob
import os
import numpy as np
np.set_printoptions(threshold=25)
import scipy.fftpack
from PIL import Image
import pandas as pd
import time
start = time.time()

def get_hash(frame_path, hash_size = 11, high_freq_factor=6):
    im = Image.open(frame_path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    hash = [1 if x == True else 0 for x in diff.flatten()]
    return hash, im


video = 'trailer_1'
multiple_videos = True

if 'trailer' in video:
    wd = '/home/emsala/Documenten/Studie/These/dataset-maken/dataset/trailers'
    video_wd = wd + '/' + video + '/' + 'trailer'
else:
    wd = '/home/emsala/Documenten/Studie/These/dataset-maken/dataset/films'
    video_wd = wd + '/' + video + '/' + 'film'

frames_wd = wd + '/' + video + '/' + 'frames'
hashes_wd = wd + '/' + video + '/' + 'hashes'

videos = glob.glob(video_wd + '/*')
videos = [video.split('/')[-1] for video in videos if video.endswith('.py') == False]
video_names = [video[0:6] for video in videos]

print(video_names)



for video_name in video_names:
    if multiple_videos:
        path = frames_wd + '/' + '{}-frames'.format(video_name)
    else:
        path = frames_wd

    video_frames = glob.glob(path + '/*')
    hashes = []
    ims = []
    frame_names = []
    for video_frame in video_frames:
        frame_name = video_frame.split('/')[-1]
        frame_names.append(frame_name)

        hash, im = get_hash(video_frame)
        hashes.append(hash)
        ims.append(im)

    data = {'video_name': [video_name] * len(hashes),
            'frame': frame_names,
            'hash': hashes,
            'im': ims}
    df = pd.DataFrame.from_dict(data)
    if multiple_videos:
        os.mkdir(hashes_wd + '/' + '{}-hashes'.format(video_name))
        os.chdir(hashes_wd + '/' + '{}-hashes'.format(video_name))
    else:
        os.chdir(hashes_wd)
    df.to_csv('{}-hashes.csv'.format(video_name))



end = time.time()
print(end - start)
print(len(hashes))



