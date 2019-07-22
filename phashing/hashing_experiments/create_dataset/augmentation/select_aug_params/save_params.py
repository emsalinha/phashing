import glob
import numpy as np
import pickle
from create_dataset.augmentation.select_aug_params.select_params import select_parameters

def save_params(img_paths, color, method):
    """

    :param img_paths: paths to all the images of the augmentation dataset
    :param color: multiscale or uniscale
    :param method: augmentation method
    :return: dict with keys = ssim and values = mean and standard deviation of the parameters of all images
    """
    param_moments = {}
    i = 0
    for img_path in img_paths:
        print(i)
        i += 1
        selected_parameters = select_parameters(img_path, color, method)
        for ssim, param in selected_parameters.items():
            if ssim in param_moments.keys():
                param_moments[ssim].append(param)
            else:
                param_moments[ssim] = [param]

    return param_moments


def compare_params(method):

    param_moments = {}

    with open('aug_params/{}_params.pickle'.format(method), 'rb') as handle:
        paths_params = pickle.load(handle)

    for ssim, params in paths_params.items():
        mean, std = np.array(params).mean(), np.array(params).std()
        param_moments[ssim] = [mean, std]

    return param_moments

def main(methods):

    sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
    img_paths = sorted(glob.glob(sample_folder + '*'))

    color = True



    for method in methods:
        paths_params = save_params(img_paths, color, method)

        with open('aug_params/{}_params.pickle'.format(method), 'wb') as handle:
            pickle.dump(paths_params, handle, protocol=pickle.HIGHEST_PROTOCOL)

        param_moments = compare_params(method)

        with open('aug_params/{}_param_moments.pickle'.format(method), 'wb') as handle:
            pickle.dump(param_moments, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    methods = ['add', 'gauss', 'compress', 'subtract_hsv', 'add_hsv', 'contrast', 'subtract']
    methods = ['compress']
    main(methods)