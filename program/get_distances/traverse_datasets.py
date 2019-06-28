import h5py
import numpy as np


def traverse_datasets(hdf_file):

    def h5py_dataset_iterator(g, prefix=''):
        for key in g.keys():
            item = g[key]
            path = f'{prefix}/{key}'
            if isinstance(item, h5py.Dataset): # test for dataset
                yield (path, item)
            elif isinstance(item, h5py.Group): # test for group (go down)
                yield from h5py_dataset_iterator(item, path)

    with h5py.File(hdf_file, 'r') as f:
        for path, _ in h5py_dataset_iterator(f):
            yield path


def read_distances(path, i):
    hists = h5py.File(path, 'r')
    datasets = []
    for dataset in traverse_datasets(path):
        datasets.append(dataset)
    return datasets[i], np.array(hists[datasets[i]])
