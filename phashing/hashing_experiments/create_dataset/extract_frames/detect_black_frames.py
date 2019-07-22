from PIL import Image
import numpy as np

def black_frame(img_path, img_size = 8):
    img = Image.open(img_path)
    img = img.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    img = np.asarray(img)
    black = np.all(img==0)
    return black


