import numpy as np
import scipy
from PIL import Image
import scipy.fftpack as scf


def DCT_hash(frame_path, hash_size=8, high_freq_factor=4):
    # """phash function from the github phash library for python"""
    im = Image.open(frame_path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    dct = scf.dct(scf.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    hash = [1 if x == True else 0 for x in diff.flatten()]
    return hash

def AVG_hash(frame_path, hash_size=8, vertical=0, horizontal=0):
    im = Image.open(frame_path)
    img_size = (hash_size + horizontal, hash_size + vertical)
    image = im.convert("L").resize(img_size, Image.ANTIALIAS)
    pixels = np.asarray(image)
    avg = pixels.mean()
    diff = pixels > avg
    out = [1 if x == True else 0 for x in diff]
    return out


