import cv2
import glob
import argparse
from PIL import Image
import numpy as np

def show_frames(config):

    for frame_path in sorted(glob.glob(config.path)):
        frame = config.path.split('/')[-1]
        img = Image.open(frame_path)
        img = np.asarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        cv2.imshow('{}'.format(frame), img)
        cv2.waitKey()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='path to images')
    config = parser.parse_args()
    show_frames(config)
