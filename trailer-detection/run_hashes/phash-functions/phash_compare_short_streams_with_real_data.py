import numpy as np
from scipy.spatial.distance import cosine, hamming, jaccard
from fastdtw import fastdtw
from phash.phash_functies import get_video_hash_list_stream, hamming_distance_2_hash_lists, return_images, get_results_frame_by_frame


path_video_stream = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/samen/*'

selection_frequency = 1
hash_size = 8
high_freq_factor = 4

method = 'hash'
distancemetric = hamming

selection_filepathnamelist_1, movie_hashes_1, movie_hashes_simple_1 = get_video_hash_list_stream(path_video_stream, selection_frequency, selection='first_half')

selection_filepathnamelist_lists , movie_hashes_lists , movie_hashes_simple_lists = get_video_hash_list_stream(path_video_stream, selection_frequency,  selection='chunks', chunksize = 10)

for movie_hashes in movie_hashes_lists:
    distans, path = fastdtw(movie_hashes, movie_hashes_1, radius = 1000, dist=distancemetric)
    print(distans, path)


#
# import matplotlib.pyplot as plt
#
# def onclick(event):
#     if event.dblclick:
#         print(plotresults[int(np.round(event.ydata)), int(np.round(event.xdata))])
#         print(selection_filepathnamelist_1[int(np.round(event.ydata))], selection_filepathnamelist_2[int(np.round(event.xdata))])
#         return_images(selection_filepathnamelist_1, event.xdata, event.ydata, selection_filepathnamelist_2)
#
#
#
# f= plt.figure()
# ax = f.add_subplot(111)
# ax.set_title('2 hours of morning RTL')
# ax.set_ylabel('minutes')
# ax.set_xlabel('minutes')
# ax.imshow(plotresults)
#
# cid = f.canvas.mpl_connect('button_press_event', onclick)
# plt.show()
# #plt.savefig('results_phash_real_data', dpi=1000)
#
# import matplotlib.pyplot as plt
#
# def onclick(event):
#     if event.dblclick:
#         print(plotresults[int(np.round(event.ydata)), int(np.round(event.xdata))])
#         print(selection_filepathnamelist_1[int(np.round(event.ydata))], selection_filepathnamelist_2[int(np.round(event.xdata))])
#         return_images(selection_filepathnamelist_1, event.xdata, event.ydata, selection_filepathnamelist_2)
#
#
#
# f= plt.figure()
# ax = f.add_subplot(111)
# ax.set_title('2 hours of morning RTL')
# ax.set_ylabel('minutes')
# ax.set_xlabel('minutes')
# ax.imshow(plotresults)
#
# cid = f.canvas.mpl_connect('button_press_event', onclick)
# plt.show()


#plt.savefig('results_phash_real_data', dpi=1000)


