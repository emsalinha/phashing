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