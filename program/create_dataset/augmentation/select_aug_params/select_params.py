import glob
from skimage.measure import compare_ssim as ssim

from create_dataset.augmentation.select_aug_params.return_augmenter import return_augmenter, return_param_range
from create_dataset.augmentation.select_aug_params.show_params import show_params

from create_dataset.augmentation.select_aug_params.MSSIM.MSSIM import MultiScaleSSIM
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image


def select_parameters(path, color, method):
    param_range = return_param_range(method)
    selected_parameters = {}
    ssim_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    for parameter in param_range:
        augmenter = return_augmenter(parameter, method)

        img = open_image(path, color=color)
        aug_img = augmenter.augment_images(img)

        ssim_const = round(MultiScaleSSIM(img, aug_img), 1)
        for i in ssim_values:
            if ssim_const == i:
                selected_parameters[i] = parameter
                ssim_values.pop(ssim_values.index(i))
                #print(selected_parameters)

        if len(ssim_values) < 1:
            break

    return selected_parameters


if __name__ == '__main__':
    sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
    sample_paths = sorted(glob.glob(sample_folder + '*'))
    n = 18
    color = True
    method = 'contrast'

    selected_parameters = select_parameters(sample_paths[n], color, method)
    show_params(selected_parameters, sample_paths[n], color=color, method=method)