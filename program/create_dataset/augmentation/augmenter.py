import logging
import pickle
import random

import cv2
import numpy as np
from PIL import Image
from imgaug import augmenters as iaa


class AugmentationMethods():

    def __init__(self):
        self.add = None
        self.gaussian_noise = None
        self.compression = None
        self.hue_and_saturation = None
        self.gamma_contrast = None
        self.methods = {}

        self.param_range_add = range(-255, 255)
        self.param_range_gauss = range(-1000, 1000)
        self.param_range_compression = [float(param)/float(100) for param in range(8000, 10000, 10)]
        self.param_range_hue = range(-255, 255)
        self.param_range_contrast = [param/10 for param in range(1, 100)]


    def init_add(self, parameter):
        self.add = iaa.Add(parameter, True)
        self.methods['add'] = self.add

    def init_gauss(self, parameter):
        self.gaussian_noise = iaa.AdditiveGaussianNoise(0, parameter, True)
        self.methods['gaussian_noise'] = self.gaussian_noise

    def init_compression(self, parameter):
        self.compression = iaa.JpegCompression(parameter)
        self.methods['compression'] = self.compression

    def init_hue(self, parameter):
        self.hue_and_saturation = iaa.AddToHueAndSaturation(parameter, True)
        self.methods['hue_and_saturation'] = self.hue_and_saturation

    def init_contrast(self, parameter):
        self.gamma_contrast = iaa.GammaContrast(parameter, False)
        self.methods['gamma_contrast'] = self.gamma_contrast

    def clean_aug_methods(self):
        self.methods = {}

    def get_augmentation_param(self, method_name, mssim=0.8):
        """
        from saved dict gets multi-structured similarity index measurement, which goes from 0 with no similarity to 1
        with total similarity between the original image and the augmented version.
        :param mssim: subset of range(0,10)/10
        :return: aug_params
        """

        loc = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/select_aug_params/'
        with open(loc + 'aug_params/{}_param_moments.pickle'.format(method_name), 'rb') as handle:
            param_moments = pickle.load(handle)

        moments = param_moments[str(mssim)]
        mean_param = int(moments[0])

        return mean_param


class Augmenter:

    def __init__(self, aug_methods: AugmentationMethods):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.aug_methods = aug_methods
        self.augmenter = None
        self.aug_method_names = None
        self.set_augmenter(aug_methods)

    def set_augmenter(self, aug_methods: AugmentationMethods):
        methods = [method for name, method in aug_methods.methods.items()]
        self.augmenter = iaa.Sequential(methods)
        self.aug_method_names = [name for name, method in aug_methods.methods.items()]

    def clean_augmenter(self):
        self.augmenter = None
        self.aug_methods = None

    def load_img(self, img_path, img_size=100):
        img = Image.open(img_path)
        img = np.asarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_size, img_size))
        return img

    def augment_img_path(self, img_path):
        img_array = self.load_img(img_path)
        aug_img_array = self.augmenter.augment_image(img_array)
        return aug_img_array




if __name__ == "__main__":

    img_path = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/1_127-Hours_frame_050000.jpg'
    aug_methods = AugmentationMethods()

    pr = list(aug_methods.param_range_add)
    random.shuffle(pr)
    aug_methods.init_add(parameter=pr[0])
    pr = list(aug_methods.param_range_contrast)
    random.shuffle(pr)
    aug_methods.init_contrast(parameter = pr[0])

    augmenter = Augmenter(aug_methods)
    augmented_img = augmenter.augment_img_path(img_path)
    print(augmented_img)



