import numpy as np
import scipy.fftpack as scf
from PIL import Image


class Hasher:

    def __init__(self):
        self.load_frame = True
        self.hash_methods = [self.DCT_hash, self.AVG_hash]
        self.set()
        self.hash_size = None
        self.high_freq_factor = None
        self.horizontal = None
        self.vertical = None



    def set(self):
        setattr(self.DCT_hash, 'name', 'DCT')
        setattr(self.AVG_hash, 'name', 'AVG')

    def __extract_params__(self, hash_params):

        if hash_params['hash_method'].__name__ == 'DCT_hash':
                self.hash_size = hash_params['hash_size']
                self.high_freq_factor = hash_params['high_freq_factor']

        elif hash_params['hash_method'].__name__ == 'AVG_hash':
                self.hash_size = hash_params['hash_size']
                self.vertical = hash_params['vertical']
                self.horizontal = hash_params['horizontal']

    def hash(self, frame, hash_params):
        self.__extract_params__(hash_params)
        if hash_params['hash_method'].__name__ == 'DCT_hash':
            phash = self.DCT_hash(frame)
        elif hash_params['hash_method'].__name__ == 'AVG_hash':
            phash = self.AVG_hash(frame)
        return phash

    def DCT_hash(self, frame, hash_params):
        """edit of phash_own function from the github phash library for python"""
        if self.load_frame:
            pixels = self.load_DCT_frame(frame)
        else:
            pixels = frame
        dct = scf.dct(scf.dct(pixels, axis=0), axis=1)
        dctlowfreq = dct[:self.hash_size, :self.hash_size]
        med = np.median(dctlowfreq)
        diff = dctlowfreq > med
        phash = [1 if x == True else 0 for x in diff.flatten()]
        phash = np.array(phash)
        return phash

    def AVG_hash(self, frame, hash_params):
        """edit of ahash function from the github phash library for python"""
        if self.load_frame:
            pixels = self.load_AVG_frame(frame)
        else:
            pixels = frame
        avg = pixels.mean()
        diff = pixels > avg
        phash = [1 if x == True else 0 for x in diff.flatten()]
        phash = np.array(phash)
        return phash

    def load_AVG_frame(self, frame_path):
        im = Image.open(frame_path)
        img_size = (self.hash_size + self.horizontal, self.hash_size + self.vertical)
        image = im.convert("L").resize(img_size, Image.ANTIALIAS)
        pixels = np.asarray(image)
        return pixels

    def load_DCT_frame(self, frame_path):
        im = Image.open(frame_path)
        img_size = self.hash_size * self.high_freq_factor
        image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
        pixels = np.asarray(image)
        return pixels
