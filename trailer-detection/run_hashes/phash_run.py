import numpy as np
np.set_printoptions(threshold=25)
from scipy.spatial.distance import cosine, hamming, jaccard
from phash.phash_functies import get_video_hashes


wd = '/home/emsala/Documenten/Studie/These/dataset-maken/dataset/trailers'



def get_hash(path_film , hash_size = 8, high_freq_factor=4):
    """create a hash for each frame and then calculate the average hash"""
    counter =0
    hashes = []
    hashes_simple = []
    filepathnamelist = glob.glob(path_film)
    filepathnamelist = sorted(filepathnamelist, key=lambda x: int(os.path.basename(x).split('.')[0].split('frame')[-1]))
    for filepathname in filepathnamelist:
        counter += 1
        im = Image.open(filepathname)
        hash = phash_own(im, hash_size, high_freq_factor)
        hash = convert_to_binary(hash.flatten())
        hashes.append(hash)

        hash_simple = phash_simple_own(im, hash_size, high_freq_factor)
        hash_simple = convert_to_binary(hash_simple.flatten())
        hashes_simple.append(str(hash_simple))

path_film1 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_T/8000/*'
path_film2 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_T/9000/*'
path_film3 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_T/1000/*'
path_film4 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_W/1000/*'
path_film5 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_W/8000/*'
path_film6 = '/home/emsala/Documenten/Media Distillery/replay-recognition/youtube-dataset/CD_W/9000/*'

paths = [path_film1, path_film2, path_film3, path_film4, path_film5, path_film6]

movie_vectors, movie_vectors_simple = get_video_hashes(paths)
print(movie_vectors)

results = []
results2 = []
for index in range(0, len(movie_vectors)):
    for index_2 in range(0, len(movie_vectors)):
        distance = cosine(movie_vectors[index], movie_vectors[index_2])
        distance2 = hamming(movie_vectors[index], movie_vectors[index_2])
        distance3 = jaccard(movie_vectors[index], movie_vectors[index_2])
        #distance2 = 1-(float(np.dot(movie_vectors[index],movie_vectors[index_2]) / (np.linalg.norm(movie_vectors[index]) * np.linalg.norm(movie_vectors[index_2]))))
        results.append([index, index_2, distance])

for result in results:
    print(result)
#
# [0, 0, 0.0]
# [0, 1, 0.38660438491785198]
# [0, 2, 0.45553449351952913]
# [0, 3, 0.45791783513634354]
# [0, 4, 0.56653927656849468]
# [0, 5, 0.57437173462062563]
# [1, 0, 0.38660438491785198]
# [1, 1, 0.0]
# [1, 2, 0.41962956930091899]
# [1, 3, 0.41731436741661621]
# [1, 4, 0.40700054667111907]
# [1, 5, 0.55964757703601031]
# [2, 0, 0.45553449351952913]
# [2, 1, 0.41962956930091899]
# [2, 2, 0.0]
# [2, 3, 0.4181426345482876]
# [2, 4, 0.40784347453620795]
# [2, 5, 0.50253166183690889]
# [3, 0, 0.45791783513634354]
# [3, 1, 0.41731436741661621]
# [3, 2, 0.4181426345482876]
# [3, 3, 0.0]
# [3, 4, 0.54378943587666229]
# [3, 5, 0.43142646731582246]
# [4, 0, 0.56653927656849468]
# [4, 1, 0.40700054667111907]
# [4, 2, 0.40784347453620795]
# [4, 3, 0.54378943587666229]
# [4, 4, 0.0]
# [4, 5, 0.53708995011372429]
# [5, 0, 0.57437173462062563]
# [5, 1, 0.55964757703601031]
# [5, 2, 0.50253166183690889]
# [5, 3, 0.43142646731582246]
# [5, 4, 0.53708995011372429]
# [5, 5, 0.0]