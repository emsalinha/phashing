from create_dataset.augmentation.augmenter import Augmenter, AugmentationMethods
from create_dataset.hashing.hasher import Hasher, DCTHash, AVGHash
from create_dataset.augmentation.augmented_hash_generator import AugmentedHashGenerator
import glob
import random
import os

img_paths = glob.glob('/home/emsala/Documenten/Studie/These/phashing/program/'
                      'create_dataset/augmentation/sample_frames/sampled_frames/*')

hasher = DCTHash()
aug_methods = AugmentationMethods()

pr = list(aug_methods.param_range_add)
random.shuffle(pr)
aug_methods.init_add(parameter=pr[0])
pr = list(aug_methods.param_range_contrast)
random.shuffle(pr)
aug_methods.init_contrast(parameter=pr[0])

augmenter = Augmenter(aug_methods)

output_path = os.getcwd()

augmentedhasher = AugmentedHashGenerator(img_paths, output_path, augmenter, hasher)
augmentedhasher.generate_augmented_hashes(save=False)
aug_hashes = augmentedhasher.augmented_hashes