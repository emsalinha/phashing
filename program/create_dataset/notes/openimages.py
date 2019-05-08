from PIL import Image
import glob
import os
import numpy as np
import cv2

cwd = os.getcwd()
cwd = cwd + '/*'

fpl = glob.glob(cwd)
for f in fpl:
    i = fpl.index(f)
    if i == 0 or i%5 == 0:
        for f2 in fpl:
            j = fpl.index(f2)
            if j == 0 or j%5 ==0:
                name = os.path.basename(f)
                name2 = os.path.basename(f2)
                img = cv2.imread(name, 1)
                img2 = cv2.imread(name2, 1)
                merged_img = np.hstack((img, img2))
                cv2.imshow('image', merged_img)
                if i != 0:
                    index1 = i/5
                else:
                    index1 = i
                if j !=0:
                    index2 = j
                else:
                    index2 = j/5
                print(index1, index2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
