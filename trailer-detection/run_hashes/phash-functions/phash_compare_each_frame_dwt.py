import numpy as np
from scipy.spatial.distance import hamming, jaccard
from fastdtw import fastdtw
from phash.phash_functies import get_video_hash_list

path_film1 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/1/framerate-900/*'
path_film2 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/1/framerate-1000/*'

path_film3 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/2/framerate-900/*'
# path_film4 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/orf-praatprogramma/2/framerate-1000/*'

path_film4 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/1/framerate-900/*'
# path_film6 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/1/framerate-1000/*'
#
# path_film7 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/2/framerate-900/*'
# path_film8 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/rtl-soap/2/framerate-1000/*'

path_film5 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-9000/*'

path_film6 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-10000/*'
path_film7 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/10-07/fr-9000-deleted-start-end/*'

path_film8 = '/home/emsala/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/11-07/fr-9000/*'

hash_size = 8
high_freq_factor = 4
method = 'hash'


hashlist1, hashlist1simple = get_video_hash_list(path_film1, method, hash_size, high_freq_factor)
hashlist2, hashlist2simple = get_video_hash_list(path_film2, method, hash_size, high_freq_factor)
hashlist3, hashlist3simple = get_video_hash_list(path_film3, method, hash_size, high_freq_factor)
hashlist4, hashlist4simple = get_video_hash_list(path_film4, method, hash_size, high_freq_factor)
hashlist5, hashlist5simple = get_video_hash_list(path_film5, method, hash_size, high_freq_factor)
hashlist6, hashlist6simple = get_video_hash_list(path_film6, method, hash_size, high_freq_factor)
hashlist7, hashlist7simple = get_video_hash_list(path_film7, method, hash_size, high_freq_factor)
hashlist8, hashlist8simple = get_video_hash_list(path_film8, method, hash_size, high_freq_factor)


print('\nDynamic time warping: \n')
hash1 = np.array(hashlist1)#[:25])
hash2 = np.array(hashlist2)#[:25])
hash3 = np.array(hashlist3)#)#[:25])
hash4 = np.array(hashlist4)#[:25])
hash5 = np.array(hashlist5)#[:160])
hash6 = np.array(hashlist6)#[:160])
hash7 = np.array(hashlist7)#[:160])
hash8 = np.array(hashlist8)#[:160])

distancemetric = hamming
#distancemetric = jaccard

print('Different framerates, same show: ')
distans, path = fastdtw(hash1, hash2, dist=distancemetric)
print(distans)

print('Different part of show: ')
distans, path = fastdtw(hash1, hash3, dist=distancemetric)
print(distans)

print('Different show: ')
distans, path = fastdtw(hash1, hash4, dist=distancemetric)
print(distans)

print('With and without intro/outro: ')
distans, path = fastdtw(hash5, hash7, dist=distancemetric)
print(distans)

print('Different show, but very similar (news day after): ')
distans, path = fastdtw(hash5, hash8, dist=distancemetric)
print(distans)


