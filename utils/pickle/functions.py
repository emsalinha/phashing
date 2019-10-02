import pickle


def open_pickle(path):
    with open(path, 'rb') as handle:
        return pickle.load(handle)