#TODO: select 1 hash type to augment
#TODO: get objective comparison hash type
import glob
import os
import pickle
from typing import List
import random
from create_dataset.augmentation.augmenter import Augmenter, AugmentationMethods
from create_dataset.hashing.hasher import Hasher, DCTHash, AVGHash


class AugmentedHashGenerator:

    def __init__(self, img_paths, output_path, augmenter: Augmenter, hasher: Hasher):
        self.params_dir = str()
        self.img_paths = img_paths
        self.augmenter = augmenter
        self.hasher = hasher
        self.output_path = output_path

        self.params_dir = '~/movie-drive/results/'
        self.augmented_hashes = []


    def set_img_paths(self, img_paths: List):
        self.img_paths = img_paths

    def set_output_path(self, output_path: str):
        self.output_path = output_path

    def set_hash_params(self, hash_params: dict):
        self.hasher.set_params(hash_params)

    def set_augmenter(self, augmenter: Augmenter):
        self.augmenter = augmenter
        #TODO: change to aug sequence?

    def set_hash_method(self, hasher: Hasher):
        self.hasher = hasher

    def get_hash_method(self):
        self.hasher.__class__.__name__
        #TODO: does this give name of abc class or of subclass?

    def get_aug_methods(self):
        return self.augmenter.aug_methods.methods

    def generate_augmented_hashes(self, color=True, save=True):

        hash_method = self.get_hash_method()
        aug_methods = self.get_aug_methods()

        print('hash method = {} and augmentation method = {}'.format(hash_method, aug_methods))

        self.augmented_hashes = []

        for image_path in sorted(self.img_paths):

            aug_img_array = self.augmenter.augment_img_path(image_path)
            phash_aug = self.hasher.phash(aug_img_array, load_img=False)

            self.augmented_hashes.append(phash_aug)

        if save:
            file_path = self.output_path + 'hashes.pickle'
            with open(file_path, 'wb') as handle:
                pickle.dump(self.augmented_hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #TODO make h5py
        #return  self.augmented_hashes




if __name__ == '__main__':

    img_paths = glob.glob('/home/emsala/Documenten/Studie/These/phashing/program/'
                                  'create_dataset/augmentation/sample_frames/sampled_frames/*')

    hasher = DCTHash()
    aug_methods = AugmentationMethods()

    pr = list(aug_methods.param_range_add)
    random.shuffle(pr)
    aug_methods.init_add(parameter=pr[0])
    pr = list(aug_methods.param_range_contrast)
    random.shuffle(pr)
    aug_methods.init_contrast(parameter = pr[0])

    augmenter = Augmenter(aug_methods)

    aug_methods = ['add_hsv', 'subtract_hsv', 'add', 'gauss', 'compress', 'contrast', 'subtract', None]

    output_path = os.getcwd()

    augmentedhasher = AugmentedHashGenerator(img_paths, output_path, augmenter, hasher)
    augmentedhasher.generate_augmented_hashes(save=False)
    aug_hashes = augmentedhasher.augmented_hashes