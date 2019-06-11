import pickle
import glob
import cv2
from create_dataset.augmentation.select_aug_params.read_params import read_params
from create_dataset.augmentation.select_aug_params.return_augmenter import return_augmenter
from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
from create_dataset.hashing.hash_functions import DCT_hash, AVG_hash

def augment_and_hash(img_path, hash_method, aug_method, param, color=True):
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

def main(image_paths, hash_methods, aug_methods, color=True):

    for hash_method in hash_methods:

        for aug_method in aug_methods:

            print(hash_method.__name__, ' ', aug_method)

            hashes = {}

            if aug_method == None:
                hashes = []
                for image_path in sorted(image_paths):
                    phash = hash_method(image_path, load_frame=True)
                    hashes.append(phash)

            else:
                param_moments = read_params(aug_method)
                for ssid, moments in param_moments.items():
                    mean_param = int(moments[0])

                    phashes_aug = []
                    for image_path in sorted(image_paths):
                        phash_aug = augment_and_hash(image_path, hash_method, aug_method, param=mean_param, color=color)
                        phashes_aug.append(phash_aug)

                    hashes[ssid] = phashes_aug

            with open('{}/{}_hashes.pickle'.format(hash_method.__name__, aug_method), 'wb') as handle:
                pickle.dump(hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
    aug_methods = [ 'add_hsv', 'subtract_hsv', 'add', 'gauss', 'compress', 'contrast', 'subtract', None]
    image_paths = glob.glob('/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/*')
    hash_methods = [DCT_hash, AVG_hash]
    #main(image_paths, hash_methods, aug_methods)
    main(image_paths, [AVG_hash], ['add_hsv', 'subtract_hsv', 'add', 'gauss', 'compress', 'contrast', 'subtract'])