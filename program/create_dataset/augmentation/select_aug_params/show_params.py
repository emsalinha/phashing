import os
import glob
import argparse
import pickle

from create_dataset.augmentation.select_aug_params.return_augmenter import return_augmenter
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
from create_dataset.augmentation.select_aug_params.MSSIM.show_images import show_images
from create_dataset.augmentation.select_aug_params.MSSIM.MSSIM import MultiScaleSSIM
from create_dataset.augmentation.select_aug_params.select_params import select_parameters

def show_params(selected_parameters, path, color, method=''):
    for parameter in selected_parameters.values():
        augmenter = return_augmenter(parameter, method)
        img = open_image(path, hash_size=15, high_freq_factor=10, color=color)
        aug_img = augmenter.augment_images(img)
        MSSIM = MultiScaleSSIM(img, aug_img)
        show_images(img, aug_img, MSSIM, color, method)


def main(n):
    sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
    sample_paths = sorted(glob.glob(sample_folder + '*'))
    img_path = sample_paths[n]

    color = True

    methods = ['subtract_hsv']

    augment_params = {}

    for method in methods:
        selected_params = select_parameters(img_path, color, method)
        augment_params['method'] = selected_params

        show_params(selected_params, img_path,  color=color, method=method)



if __name__ == "__main__":
    main(22)
