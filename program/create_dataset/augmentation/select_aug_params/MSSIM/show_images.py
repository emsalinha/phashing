import cv2
import numpy as np


def show_images(img1, img2, MSSIM, color=False, method=''):
    if color==False:
        img1 = np.squeeze(img1, axis=3)
        img2 = np.squeeze(img2, axis=3)

    img1 = np.squeeze(img1, axis=0)
    img2 = np.squeeze(img2, axis=0)
    images = np.concatenate((img1, img2), axis=1)
    cv2.imshow('MSSIM: {}, method: {}'.format(MSSIM, method), images)
    cv2.waitKey()

