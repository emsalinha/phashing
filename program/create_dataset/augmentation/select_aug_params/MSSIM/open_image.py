from PIL import Image
import numpy as np
import cv2


def open_image(frame_path, hash_size=8, high_freq_factor=4, color=False, hash_method = 'DCT_hash'):
    if hash_method == 'DCT_hash':
        img_size = int(hash_size * high_freq_factor)
    elif hash_method == 'AVG_hash':
        img_size = hash_size
    else:
        print('unknown hash_method')
        img_size = 8
    if color:
        image = color_test_image(frame_path, img_size)
    else:
        image = gray_hash_image(frame_path, img_size)
    return image

def gray_hash_image(frame_path, img_size):
    img = Image.open(frame_path)
    img = img.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    img = np.asarray(img)
    img = np.expand_dims(img, axis=3)
    img = np.expand_dims(img, axis=0)
    return img

def color_test_image(frame_path, img_size):
    img = Image.open(frame_path)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(img_size, img_size))
    img = np.expand_dims(img, axis=0)
    return img

