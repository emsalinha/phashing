from PIL import Image
import numpy as np
from create_dataset.hashing.hash_functions import DCT_hash

def black_frame(img_path, img_size = 8):
    img = Image.open(img_path)
    img = img.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    img = np.asarray(img)
    black = np.all(img==0)
    return black

def black_hash(img_path):
    phash = DCT_hash(img_path)
    black = np.all(phash == 0)
    return black

if __name__ == '__main__':
    phash = black_hash('frame_000000.jpg')
    print(phash)