import h5py
import numpy as np
import time

def hash_and_write(movie_name, frame_paths, hash_method, hash_params):
    """
    writes hashes one by one to a (newly created) HDF5 file in the working directory
    :param movie_name: 'movie name'
    :param frame_paths: [paths to frames in movie]
    :param hash_method: DCT or average hash
    :param hash_params: {augmentation, hash_size, high_freq_factor, vertical, horizontal}
    :return time spend per hash
    :output hdf5 file: /augmentation/hash_method/hash_size
    """
    total_time = 0

    hash_len = hash_params['hash_size'] * hash_params['hash_size']
    n_frames = len(frame_paths)
    data_size = (n_frames, hash_len)
    phashes = np.zeros(data_size)

    if hash_params['augmentation']:
        group_name = 'augmented'
    else:
        group_name = 'unaugmented'
    subgroup_name = hash_method.__name__
    subsubgroup_name = hash_params['hash_size']
    dataset_name = '{}/{}/{}'.format(group_name, subgroup_name, subsubgroup_name)

    hdf5_store = h5py.File('hashes_{}.hdf5'.format(movie_name), 'a')

    phashes = hdf5_store.create_dataset(dataset_name, phashes.shape, compression='gzip')

    for i in range(0, n_frames):
        frame_path = frame_paths[i]
        start = time.time()
        phash = hash_method(frame_path, hash_params)
        end = time.time()
        total_time += (end-start)
        phashes[i] = phash

    return total_time/n_frames
