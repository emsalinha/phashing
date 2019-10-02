import numpy as np
import scipy.fftpack as scf
from PIL import Image
import logging
import abc
import cv2

class Hasher(abc.ABC):

    def __init__(self, hash_params=None):

        self.hash_params = {
            'hash_method': self.__class__.__name__,
            'augmentation': None,
            'hash_size': 12,
            'high_freq_factor': 8,
            'vertical': 0,
            'horizontal': 0
        }

        if hash_params != None:
            self.hash_params = hash_params

    def set_params(self, hash_params: dict):
        self.hash_params = hash_params


    def phash(self, img, load_img=True):

        if load_img:
            img_path = img
            img_array = self.__load_frame__(img_path)

        else:
            img_array = img
            img_array = self.__remove_colour__(img_array)

        phash = self.__phash_array__(img_array)
        return phash

    def __remove_colour__(self, img_array):

        if len(img_array.shape) > 2:
            if img_array.shape[2] > 1:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

            else:
                img_array = img_array.squeeze(axis=2)

        return img_array



    @abc.abstractmethod
    def __load_frame__(self, img_path):
        pass

    @abc.abstractmethod
    def __phash_array__(self, img):
        pass


class DCTHash(Hasher):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)


    def __phash_array__(self, pixels):

        hash_size = self.hash_params['hash_size']
        """edit of phash_own function from the github phash library for python"""
        dct = scf.dct(scf.dct(pixels, axis=0), axis=1)
        dctlowfreq = dct[:hash_size, :hash_size]
        med = np.median(dctlowfreq)
        diff = dctlowfreq > med
        phash = [1 if x == True else 0 for x in diff.flatten()]
        phash = np.array(phash)
        return phash

    def __load_frame__(self, frame_path):
        hash_size = self.hash_params['hash_size']
        high_freq_factor = self.hash_params['high_freq_factor']

        im = Image.open(frame_path)
        img_size = hash_size * high_freq_factor
        image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
        pixels = np.asarray(image)
        return pixels


class AVGHash(Hasher):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def __phash_array__(self, pixels):

        """edit of ahash function from the github phash library for python"""
        avg = pixels.mean()
        diff = pixels > avg
        phash = [1 if x == True else 0 for x in diff.flatten()]
        phash = np.array(phash)
        return phash

    def __load_frame__(self, frame_path):
        hash_size = self.hash_params['hash_size']
        vertical = self.hash_params['vertical']
        horizontal = self.hash_params['horizontal']

        im = Image.open(frame_path)
        img_size = (hash_size + horizontal, hash_size + vertical)
        image = im.convert("L").resize(img_size, Image.ANTIALIAS)
        pixels = np.asarray(image)
        return pixels


if __name__ == "__main__":

    img_path = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/1_127-Hours_frame_050000.jpg'
    dct_hasher = DCTHash()
    phash = dct_hasher.phash(img_path, load_img=True)
    print(phash.shape)
    params = dct_hasher.hash_params
    params['hash_size'] = 8
    dct_hasher.set_params(params)
    phash = dct_hasher.phash(img_path, load_img=True)
    print(phash.shape)

