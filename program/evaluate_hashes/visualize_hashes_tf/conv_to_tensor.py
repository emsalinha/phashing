import torch
import glob
import pandas as pd
import csv
import os
import numpy as np
from PIL import Image
import h5py
from tensorboardX import SummaryWriter
writer = SummaryWriter()

movie_hashes_path = '/home/emsala/movie-drive/hashes/00_12-Angry-Men/annotated_hashes_00_12-Angry-Men.hdf5'
trailer_hashes_path = '/home/emsala/movie-drive/trailer_hashes/0_12-Angry-Men_trailer/hashes_0_12-Angry-Men_trailer.hdf5'

ds_name_movie = '/unaugmented/DCT_hash/12/hashes'
ds_name_trailer = '/unaugmented/DCTHash/12/hashes'

h5store_movie = h5py.File(movie_hashes_path, 'r')
h5store_trailer = h5py.File(trailer_hashes_path, 'r')


hashes_movie = h5store_movie[ds_name_movie][:]
hashes_trailer = h5store_trailer[ds_name_trailer][:]


hashes = np.vstack((hashes_movie, hashes_trailer))
hashes = torch.from_numpy(hashes)

trailer_frames_dir = '/home/emsala/movie-drive/frames/01_andere_vid'
movie_frames_dir = '/home/emsala/movie-drive/frames/02_mijn_vid'

trailer_frame_paths = glob.glob(trailer_frames_dir + '/*')
movie_frame_paths = glob.glob(movie_frames_dir + '/*')

n_hashes = hashes.shape[0]
frame_paths = []
paths = (movie_frame_paths + trailer_frame_paths) * 2000

for path in paths:
    while len(frame_paths) < n_hashes:
        frame_paths.append(path)
    break


hash_size = 12
high_freq_factor=8
images = []
for path in frame_paths:
    im = Image.open(path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    images.append(image)

images = torch.from_numpy(np.array(images))

writer.add_embedding(hashes, label_img=images) #metadata=labels



