#TODO: select 1 hash type to augment
#TODO: get objective comparison hash type


def main(config):

  if config.VM:
    from select_aug_params.MSSIM.MSSIM import MultiScaleSSIM
    from select_aug_params.MSSIM.open_image import open_image
    from select_aug_params.MSSIM.show_images import show_images
    params_dir = '/movie-drive/results/'


  else:
    from create_dataset.augmentation.select_aug_params.MSSIM.show_images import show_images
    from create_dataset.augmentation.select_aug_params.MSSIM.open_image import open_image
    from create_dataset.augmentation.select_aug_params.MSSIM.MSSIM import MultiScaleSSIM
    params_dir = '~/movie-drive/results/'

    

    sample_folder = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/sample_frames/sampled_frames/'
    sample_paths = sorted(glob.glob(sample_folder + '*'))
    n = 18
    img_path = sample_paths[n]

  with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)



def main(_):
  if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
    config = parser.parse_args()
    main(config)

