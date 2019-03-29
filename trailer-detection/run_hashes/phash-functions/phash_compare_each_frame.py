import numpy as np
from scipy.spatial import distance
from fastdtw import fastdtw
from phash_analysis.phash_functies import get_video_hash_list, hamming_distance_2_hash_lists

# path_film1 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/1/framerate-900/*'
# path_film2 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/1/framerate-1000/*'
#
# path_film3 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/2/framerate-900/*'
# # path_film4 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/2/framerate-1000/*'
#
# path_film4 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/1/framerate-900/*'
# # path_film6 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/1/framerate-1000/*'
# #
# # path_film7 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/2/framerate-900/*'
# # path_film8 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/2/framerate-1000/*'

path_film5 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-9000/*'

# path_film6 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-10000/*'
# path_film7 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-9000-deleted-start-end/*'
#
# path_film8 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/11-07/fr-9000/*'

hash_size = 8
high_freq_factor = 4
method = 'hash'
#
#
# hash1, hash1simple = get_video_hash_list(path_film1, method, hash_size, high_freq_factor)
# hash2, hash2simple = get_video_hash_list(path_film2, method, hash_size, high_freq_factor)
# hash3, hash3simple = get_video_hash_list(path_film3, method, hash_size, high_freq_factor)
# hash4, hash4simple = get_video_hash_list(path_film4, method, hash_size, high_freq_factor)
hash5, hash5simple = get_video_hash_list(path_film5, method, hash_size, high_freq_factor)
# hash6, hash6simple = get_video_hash_list(path_film6, method, hash_size, high_freq_factor)
# hash7, hash7simple = get_video_hash_list(path_film7, method, hash_size, high_freq_factor)
# hash8, hash8simple = get_video_hash_list(path_film8, method, hash_size, high_freq_factor)

#function deletes a part of the hashes in the list, because it only allows for the same length

# print('Different framerates, same show: ')
# hammingdistances1 = hamming_distance_2_hash_lists(hash1, hash2)
# print('Different part of show: ')
# hammingdistances2 = hamming_distance_2_hash_lists(hash1, hash3)
# print('Different show: ')
# hammingdistances3 = hamming_distance_2_hash_lists(hash1, hash4)
# print('With and without intro/outro: ')
# hammingdistances4 = hamming_distance_2_hash_lists(hash5, hash7)
# print('Different show, but very similar (news day after): ')
# hammingdistances5 = hamming_distance_2_hash_lists(hash5, hash8)

print(hash5)
print(len(hash5))