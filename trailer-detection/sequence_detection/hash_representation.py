import logging
import numpy as np
import pywt
import scipy.fftpack
from PIL import Image

from representation_creator import RepresentationCreator


class HashRepresentationCreator(RepresentationCreator):

    def __init__(self, window_size: int, hash_method=None, hash_params=None):
        super().__init__(window_size)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.hash = hash_method
        self.hash_params = hash_params
        if hash_params is None:
            self.hash_params = default_params
        if hash_method is None:
            self.hash_method = phash

    def __create_representation__(self, frame):
        pil_image = Image.fromarray(frame)
        diff = self.hash(pil_image, self.hash_params)
        diff_flattened = diff.flatten()
        binary_vector = [1 if x else 0 for x in diff_flattened]
        binary_vector = np.array(binary_vector)
        return binary_vector


default_params = {
    "hash_size": 8,
    "highfreq_factor": 4,
    "whash_parameters": (None, 'haar', True)
}


def extract_imgsize_dct(pil_image, img_size):
    pil_image = pil_image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(pil_image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    return dct


def extract_hashsize_pixels(pil_image, hash_size, vertical=0, horizontal=0):
    pil_image = pil_image.convert("L").resize((hash_size + horizontal, hash_size + vertical), Image.ANTIALIAS)
    pixels = np.asarray(pil_image)
    return pixels


def phash(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    highfreq_factor = hash_params['highfreq_factor']
    img_size = highfreq_factor * hash_size
    dct = extract_imgsize_dct(pil_image, img_size)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    return diff


def phash_simple(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    highfreq_factor = hash_params['highfreq_factor']
    img_size = highfreq_factor * hash_size
    dct = extract_imgsize_dct(pil_image, img_size)
    dctlowfreq = dct[:hash_size, 1:hash_size + 1]
    avg = dctlowfreq.mean()
    diff = dctlowfreq > avg
    return diff


def ahash(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    pixels = extract_hashsize_pixels(pil_image, hash_size)
    avg = pixels.mean()
    diff = pixels > avg
    return diff


def dhash(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    pixels = extract_hashsize_pixels(pil_image, hash_size, horizontal=1)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff


def dhash_vertical(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    pixels = extract_hashsize_pixels(pil_image, hash_size, vertical=1)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff


def whash(pil_image, hash_params):
    hash_size = hash_params['hash_size']
    image_scale, mode, remove_max_haar_ll = hash_params['whash_parameters']

    if image_scale is not None:
        assert image_scale & (image_scale - 1) == 0, "image_scale is not power of 2"
    else:
        image_natural_scale = 2 ** int(np.log2(min(pil_image.size)))
        image_scale = max(image_natural_scale, hash_size)

    ll_max_level = int(np.log2(image_scale))

    level = int(np.log2(hash_size))
    assert hash_size & (hash_size - 1) == 0, "hash_size is not power of 2"
    assert level <= ll_max_level, "hash_size in a wrong range"
    dwt_level = ll_max_level - level

    pil_image = pil_image.convert("L").resize((image_scale, image_scale), Image.ANTIALIAS)
    pixels = np.asarray(pil_image) / 255

    # Remove low level frequency LL(max_ll) if @remove_max_haar_ll using haar filter
    if remove_max_haar_ll:
        coeffs = pywt.wavedec2(pixels, 'haar', level=ll_max_level)
        coeffs = list(coeffs)
        coeffs[0] *= 0
        pixels = pywt.waverec2(coeffs, 'haar')

    # Use LL(K) as freq, where K is log2(@hash_size)
    coeffs = pywt.wavedec2(pixels, mode, level=dwt_level)
    dwt_low = coeffs[0]

    # Substract median and compute hash
    med = np.median(dwt_low)
    diff = dwt_low > med
    return diff
