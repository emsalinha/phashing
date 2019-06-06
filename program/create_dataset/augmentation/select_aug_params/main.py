from create_dataset.augmentation.select_aug_params.select_params import select_parameters
from create_dataset.augmentation.select_aug_params.show_params import show_params
import glob

sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
sample_paths = sorted(glob.glob(sample_folder + '*'))
n = 18

path = sample_paths[18]

color = True

methods = ['add', 'gauss', 'compress', 'subtract_hsv', 'add_hsv', 'contrast', 'subtract']

method_params = {}

for method in methods:
    selected_params = select_parameters(path, color, method)
    method_params['method'] = selected_params
    show_params(selected_params, path,  color=color, method=method)

