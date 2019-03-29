import numpy as np
from scipy.spatial.distance import cosine, hamming, jaccard
from fastdtw import fastdtw
from phash.phash_functies import get_video_hash_list_stream, hamming_distance_2_hash_lists, return_images, get_results_frame_by_frame


path_video_stream = '/home/emsala/Documenten/Media Distillery/replay-recognition/repeated-sequence-dataset/rtl4/*'

selection_frequency = 1
selection = 'total'

hash_size = 8
high_freq_factor = 4

method = 'hash'

selection_filepathnamelist, movie_hashes, movie_hashes_simple = get_video_hash_list_stream(path_video_stream, selection_frequency, selection)

results, plotresults = get_results_frame_by_frame(movie_hashes)

# distancemetric = hamming
# distans, path = fastdtw(hash1, hash2, dist=distancemetric)
# print(distans, path)


import matplotlib.pyplot as plt

def onclick(event):
    if event.dblclick:
        print(plotresults[[int(np.round(event.xdata))], int(np.round(event.ydata))])
        return_images(selection_filepathnamelist, event.xdata, event.ydata)




f= plt.figure()
ax = f.add_subplot(111)
ax.set_title('2 hours of morning RTL')
ax.set_ylabel('minutes')
ax.set_xlabel('minutes')
ax.imshow(plotresults)

cid = f.canvas.mpl_connect('button_press_event', onclick)
plt.show()
#plt.savefig('results_phash_real_data', dpi=1000)



import pandas as pd
results_df = pd.DataFrame(results)
#results_df.to_csv('results_phash_real_data.csv')