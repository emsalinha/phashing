import numpy as np
import scipy.fftpack as scf
from PIL import Image


def DCT_hash(frame_path, hash_params = None):
    """edit of phash_own function from the github phash library for python"""

    if hash_params == None:
        hash_size = 8
        high_freq_factor = 4
    else:
        hash_size = hash_params['hash_size']
        high_freq_factor = hash_params['high_freq_factor']

    im = Image.open(frame_path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    dct = scf.dct(scf.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    hash = [1 if x == True else 0 for x in diff.flatten()]
    hash = np.array(hash)
    return hash

def AVG_hash(frame_path, hash_params = None):
    """edit of ahash function from the github phash library for python"""

    if hash_params == None:
        hash_size = 8
        vertical = 0
        horizontal = 0
    else:
        hash_size = hash_params['hash_size']
        vertical = hash_params['vertical']
        horizontal = hash_params['horizontal']

    im = Image.open(frame_path)
    img_size = (hash_size + horizontal, hash_size + vertical)
    image = im.convert("L").resize(img_size, Image.ANTIALIAS)
    pixels = np.asarray(image)
    avg = pixels.mean()
    diff = pixels > avg
    hash = [1 if x == True else 0 for x in diff.flatten()]
    hash = np.array(hash)
    return hash


setattr(DCT_hash, 'name', 'DCT')
setattr(AVG_hash, 'name', 'AVG')