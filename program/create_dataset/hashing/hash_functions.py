import numpy as np
import scipy.fftpack as scf
from PIL import Image

def DCT_hash(frame, hash_params=None, load_frame=True):
    """edit of phash_own function from the github phash library for python"""
    hash_size, high_freq_factor = extract_params('DCT', hash_params)
    if load_frame:
        pixels = load_DCT_frame(frame, hash_size, high_freq_factor)
    else:
        pixels = frame
    dct = scf.dct(scf.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    hash = [1 if x == True else 0 for x in diff.flatten()]
    hash = np.array(hash)
    return hash


def AVG_hash(frame, hash_params=None, load_frame=True):
    """edit of ahash function from the github phash library for python"""
    hash_size, vertical, horizontal = extract_params('AVG', hash_params)
    if load_frame:
        pixels = load_AVG_frame(frame, hash_size, vertical, horizontal)
    else:
        pixels = frame
    avg = pixels.mean()
    diff = pixels > avg
    hash = [1 if x == True else 0 for x in diff.flatten()]
    hash = np.array(hash)
    return hash

def load_AVG_frame(frame_path, hash_size, vertical, horizontal):
    im = Image.open(frame_path)
    img_size = (hash_size + horizontal, hash_size + vertical)
    image = im.convert("L").resize(img_size, Image.ANTIALIAS)
    pixels = np.asarray(image)
    return pixels

def load_DCT_frame(frame_path, hash_size, high_freq_factor):
    im = Image.open(frame_path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    return pixels


def extract_params(method, hash_params):
    if method == 'DCT':
        if hash_params == None:
            hash_size = 12
            high_freq_factor = 4
        else:
            hash_size = hash_params['hash_size']
            high_freq_factor = hash_params['high_freq_factor']
        return hash_size, high_freq_factor

    elif method == 'AVG':
        if hash_params == None:
            hash_size = 12
            vertical = 0
            horizontal = 0
        else:
            hash_size = hash_params['hash_size']
            vertical = hash_params['vertical']
            horizontal = hash_params['horizontal']
        return hash_size, vertical, horizontal


setattr(DCT_hash, 'name', 'DCT')
setattr(AVG_hash, 'name', 'AVG')