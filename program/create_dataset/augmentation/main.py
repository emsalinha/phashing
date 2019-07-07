from create_dataset.augmentation.augmenter import Augmenter
from create_dataset.hashing.hasher import Hasher
from create_dataset.augmentation.augmented_hash_generator import AugmentedHashGenerator


augmenter = Augmenter()
augmenter.aug_methods.init_compression(.9)
augmenter.aug_methods.init_add(50)
augmenter.augment_img()


if __name__ == "__main__":

    img_path = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/1_127-Hours_frame_050000.jpg'
    dct_hasher = DCTHash()
    phash = dct_hasher.phash(img_path, load_img=True)
    print(phash.shape)
    params = dct_hasher.hash_params
    params['hash_size'] = 8
    dct_hasher.set_params(params)
    phash = dct_hasher.phash(img_path, load_img=True)
    print(phash.shape)

