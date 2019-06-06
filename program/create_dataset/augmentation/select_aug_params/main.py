import os
import glob
import argparse
import pickle

def main(config):

    if config.VM:
        img_path = '/movie-drive/frames/18_High-Voltage/frame_050000.jpg'
        home = '/movie-drive/'
        result_dir = home + 'results/'
        from select_params import select_parameters
        from show_params import show_params
    else:
        home = os.getenv('HOME') + '/movie-drive/'
        from create_dataset.augmentation.select_aug_params.select_params import select_parameters
        from create_dataset.augmentation.select_aug_params.show_params import show_params

        sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
        sample_paths = sorted(glob.glob(sample_folder + '*'))
        n = 18
        img_path = sample_paths[18]

    color = True

    methods = ['add', 'gauss', 'compress', 'subtract_hsv', 'add_hsv', 'contrast', 'subtract']

    augment_params = {}

    for method in methods:
        selected_params = select_parameters(img_path, color, method)
        augment_params['method'] = selected_params

        if config.VM == False:
            show_params(selected_params, img_path,  color=color, method=method)

    with open('augment_params.pickle', 'wb') as handle:
        pickle.dump(augment_params, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    config = parser.parse_args()
    main(config)

