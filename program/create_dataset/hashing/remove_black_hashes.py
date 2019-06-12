import numpy as np

def remove_black_hashes(hashes):
    hashes = hashes[~np.all(hashes == 0, axis=1)]
    return hashes

