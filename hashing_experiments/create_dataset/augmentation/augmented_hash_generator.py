#TODO: select 1 hash type to augment
#TODO: get objective comparison hash type
import argparse
import glob
import pickle
import glob
import cv2
from create_dataset.augmentation.select_aug_params.read_params import read_params
from create_dataset.augmentation.select_aug_params.return_augmenter import return_augmenter
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
from create_dataset.hashing.Hasher import Hasher
from create_dataset.augmentation.select_aug_params.MSSIM.show_images import show_images
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
from create_dataset.augmentation.select_aug_params.MSSIM.MSSIM import MultiScaleSSIM

#TODO: class filenames niet met hoofdletter
#TODO: class niet bij init laten runnen
#TODO: maak setter voor wijzigingen van vaste variabelen
#TODO: main zeg weinig, wat gebeurt er als je object wijzigt en dan runt,
#TODO: een gheel maken van de losstaande stappen

#TODO: enumeration maken van aug_methods, en dan invoeren als type, dan weet je welke opties er zijn,
# dat maakt t makkelijker te extenden, en hoef je maar op 1 plek aan te passen
# abstract base class maken voor augmentator
# duidelijk welke subclass er aan geroepen wordt en dat elke subclass hetzelfde loopt
#TODO: type hinting toevoegen


class AugmentedHashGenerator:

    def __init__(self, img_paths, aug_methods, output_path, hash_params=None):
        self.params_dir = str()
        self.import_modules()
        self.aug_methods = self.get_aug_methods(aug_methods)
        self.img_paths = self.get_img_paths(img_paths)
        self.params_dir = '~/movie-drive/results/'
        self.hasher = Hasher
        if hash_params is None:
            self.hash_params = {
              'method': None,
              'augmentation': True,
              'hash_size': None,
              'high_freq_factor': 8,
              'vertical': 0,
              'horizontal': 0
            }
        self.main()


    def main(self, color=True):

        for hash_method in self.hasher.hash_methods:

            for aug_method in self.aug_methods:

                print(hash_method.__name__, ' ', aug_method)

                hashes = {}

                self.hash_params['method'] = hash_method.__name__

                if aug_method == None:
                    hashes = []
                    for image_path in sorted(self.img_paths):
                        phash = self.hasher.hash(image_path, self.hash_params)
                        hashes.append(phash)

                else:
                    param_moments = read_params(aug_method)
                    for ssid, moments in param_moments.items():
                        mean_param = int(moments[0])

                    phashes_aug = []
                    for image_path in sorted(self.img_paths):
                        phash_aug = self.augment_and_hash(image_path, hash_method, aug_method, param=mean_param, color=color)
                        phashes_aug.append(phash_aug)

                    hashes[ssid] = phashes_aug

            with open('{}_12/{}_hashes.pickle'.format(hash_method.__name__, aug_method), 'wb') as handle:
              pickle.dump(hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def augment_and_hash(self, img_path, hash_method, aug_method, param, color=True):
        """
        :param img: PIL image
        :param method: augmentation method (str)
        :parameter method parameters
        :return: hashes
        """

        augmenter = return_augmenter(param, aug_method)
        img_array = open_image(img_path, color = color, hash_method = hash_method.__name__)
        aug_img_array = augmenter.augment_images(img_array)
        aug_img_array = aug_img_array.squeeze(axis = 0)
        if color:
          aug_img_array = cv2.cvtColor(aug_img_array, cv2.COLOR_RGB2GRAY)
        else:
          aug_img_array = aug_img_array.squeeze(axis=3)

        phash = hash_method(aug_img_array, load_frame=False)
        return phash



if __name__ == '__main__':

    # def get_img_paths(self, img_paths):
    #     if img_paths == None:
    #        img_paths = glob.glob('/home/emsala/Documenten/Studie/These/phashing/program/'
    #                               'create_dataset/augmentation/sample_frames/sampled_frames/*')
    #     return img_paths
    #
    # def get_aug_methods(self, aug_methods):
    #     if aug_methods == None:
    #         aug_methods = ['add_hsv', 'subtract_hsv', 'add', 'gauss', 'compress', 'contrast', 'subtract', None]
    #     return aug_methods

    augment = AugmentedHashGenerator()
