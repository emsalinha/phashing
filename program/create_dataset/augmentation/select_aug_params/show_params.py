from create_dataset.augmentation.select_aug_params.return_augmenter import return_augmenter
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
from create_dataset.augmentation.select_aug_params.MSSIM.show_images import show_images
from create_dataset.augmentation.select_aug_params.MSSIM.MSSIM import MultiScaleSSIM

def show_params(selected_parameters, path, color, method=''):
    for parameter in selected_parameters.values():
        augmenter = return_augmenter(parameter, method)
        img = open_image(path, hash_size=15, high_freq_factor=10, color=color)
        aug_img = augmenter.augment_images(img)
        MSSIM = MultiScaleSSIM(img, aug_img)
        show_images(img, aug_img, MSSIM, color, method)


