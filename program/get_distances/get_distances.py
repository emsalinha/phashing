from scipy.spatial.distance import cdist


def get_results_frame_by_frame(movie_hashes, movie_hashes_2 = None):
    if movie_hashes_2 != None:
        movie_hashes_2 = movie_hashes_2
        if len(movie_hashes) != len(movie_hashes_2):
            length = min(len(movie_hashes), len(movie_hashes_2))
            movie_hashes = movie_hashes[:length-1]
            movie_hashes_2 = movie_hashes[:length-1]
    else:
        movie_hashes_2 = movie_hashes


    results = cdist(movie_hashes, movie_hashes_2, 'hamming')
    results = 1-results
    return results

