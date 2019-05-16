import numpy as np
from scipy.spatial.distance import cosine, hamming, jaccard
from fastdtw import fastdtw
from phash_analysis.phash_functies import get_video_hash_list_stream, return_images, get_results_frame_by_frame


path_video_stream = '/home/emma/Documenten/Media Distillery/replay-recognition/repeated-sequence-dataset/rtl4/*'

selection_frequency = 100

hash_size = 6
high_freq_factor = 4

method = 'hash'

selection_filepathnamelist_1, movie_hashes_1 = get_video_hash_list_stream(path_video_stream, selection_frequency, selection='first_half', hash_size = 6)
print('volgende')
selection_filepathnamelist_2 , movie_hashes_2 = get_video_hash_list_stream(path_video_stream, selection_frequency,  selection='second_half', hash_size = 6)

for hash in movie_hashes_1:
    print(hash)
    print(len(hash))

results = get_results_frame_by_frame(movie_hashes_1, movie_hashes_2)

import matplotlib.pyplot as plt

def onclick(event):
    if event.dblclick:
        print(results[int(np.round(event.ydata)), int(np.round(event.xdata))])
        print(selection_filepathnamelist_1[int(np.round(event.ydata))], selection_filepathnamelist_2[int(np.round(event.xdata))])
        return_images(selection_filepathnamelist_1, event.xdata, event.ydata, selection_filepathnamelist_2)



f= plt.figure()
ax = f.add_subplot(111)
ax.set_title('2 hours of morning RTL')
ax.set_ylabel('each 10 sec')
ax.set_xlabel('each 10 sec')
ax.imshow(results)

cid = f.canvas.mpl_connect('button_press_event', onclick)
plt.show()
#plt.savefig('results_phash_real_data', dpi=1000)



import pandas as pd
results_df = pd.DataFrame(results)
#results_df.to_csv('results_phash_real_data.csv')


def return_images(filepathnamelist, x, y, filepathnamelist2 = None):
    import cv2
    import pylab as plt
    if len(filepathnamelist2) != None:
        filepathnamelist2 = filepathnamelist2
    else:
        filepathnamelist2 = filepathnamelist

    # get list of indeces with modulo 60 and then get new filepath name list that corresponds with x and y
    filename = os.path.basename(filepathnamelist[0])
    working_directory = filepathnamelist[0].replace(filename, '')
    os.chdir(working_directory)

    fp_img_1 = filepathnamelist[int(np.round(y))]
    fp_img_2 = filepathnamelist2[int(np.round(x))]

    name = os.path.basename(fp_img_1)
    name2 = os.path.basename(fp_img_2)

    img = cv2.imread(name, 1)
    img2 = cv2.imread(name2, 1)

    merged_img = np.hstack((img, img2))

    f = plt.figure()
    ax = f.add_subplot(111)
    ax.imshow(merged_img)
    ax.set_title('{}{}'.format(name, name2))
    plt.axis('off')
    plt.show()
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

