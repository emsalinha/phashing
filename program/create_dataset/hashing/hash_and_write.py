import time

import h5py
import numpy as np


def hash_and_write(movie_name, frame_paths, hash_method, hash_params, fps=25):
    """
    writes hashes one by one to a (newly created) HDF5 file in the working directory
    :param movie_name: 'movie name'
    :param frame_paths: [paths to frames in movie]
    :param hash_method: DCT or average hash
    :param hash_params: {augmentation, hash_size, high_freq_factor, vertical, horizontal}
    :param fps: sampled frames per second
    :return time spend per hash
    :output hdf5 file: /augmentation/hash_method/hash_size
    """
    speed = 0

    hash_len = hash_params['hash_size'] * hash_params['hash_size']
    frame_paths = frame_paths[0::fps]
    n_frames = len(frame_paths)

    ds_size_hashes = (n_frames, hash_len)
    ds_size_fps = (n_frames, )

    if hash_params['augmentation']:
        group_name = 'augmented'
    else:
        group_name = 'unaugmented'
    subgroup_name = hash_method.__name__
    subsubgroup_name = hash_params['hash_size']
    ds_name_hashes = '{}/{}/{}/hashes'.format(group_name, subgroup_name, subsubgroup_name)
    ds_name_frames = '{}/{}/{}/frames'.format(group_name, subgroup_name, subsubgroup_name)

    hdf5_store = h5py.File('annotated_hashes_{}.hdf5'.format(movie_name), 'a')
    print(ds_name_hashes)
    phashes_ds = hdf5_store.create_dataset(ds_name_hashes, ds_size_hashes, compression='gzip')
    dt = h5py.special_dtype(vlen=np.dtype('int32'))
    frame_paths_ds = hdf5_store.create_dataset(ds_name_frames, ds_size_fps, dtype=dt)

    start = time.time()

    for i in range(0, n_frames):
        phash = hash_method(frame_paths[i], hash_params)
        phashes_ds[i] = phash

        frame_nr = frame_paths[i].split('/')[-1].split('_')[1].split('.')[0]
        frame_paths_ds[i] = [int(frame_nr)]

    end = time.time()
    speed = (end-start)/n_frames

    # try:
    #     hdf5_store = h5py.File('annotated_hashes_{}.hdf5'.format(movie_name), 'a')
    #     phashes_ds = hdf5_store.create_dataset(ds_name_hashes, ds_size_hashes, compression='gzip')
    #     print(ds_name_hashes)
    #     dt = h5py.special_dtype(vlen=np.dtype('int32'))
    #     frame_paths_ds = hdf5_store.create_dataset(ds_name_frames, ds_size_fps, dtype=dt)

    #     start = time.time()

    #     for i in range(0, n_frames):
    #         phash = hash_method(frame_paths[i], hash_params)
    #         phashes_ds[i] = phash

    #         frame_nr = frame_paths[i].split('/')[-1].split('_')[0]
    #         frame_paths_ds[i] = [int(frame_nr)]

    #     end = time.time()
    #     speed = (end-start)/n_frames

    # except:
    #     print('no hashes saved')

    return speed
