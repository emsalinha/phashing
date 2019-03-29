import numpy as np
import scipy
from PIL import Image
import glob
import scipy.fftpack
import os
from scipy.spatial import distance


def get_hash(frame_path, hash_size = 8, high_freq_factor=4):
    im = Image.open(frame_path)
    img_size = hash_size * high_freq_factor
    image = im.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    hash = [1 if x == True else 0 for x in diff.flatten()]

def chunks(list, n):
    list_of_lists = []
    # For item i in a range that is a length of l,
    for i in range(0, len(list), n):
        # Create an index range for l of n items:
        list_of_lists.append(list[i:i+n])
    return list_of_lists


def dhash(image, hash_size=8):
    """
    Difference Hash computation.
    following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

    computes differences horizontally
    @image must be a PIL instance.
    """
    # resize(w, h), but numpy.array((h, w))
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    image = image.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = np.asarray(image)
    # compute differences between columns
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff

def phash_own(image, hash_size=8, highfreq_factor=4):
    #"""phash function from the github phash library for python"""
	img_size = hash_size * highfreq_factor
	image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
	pixels = np.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = np.median(dctlowfreq)
	diff = dctlowfreq > med
	return diff

def phash_simple_own(image, hash_size=8, highfreq_factor=4):
    #"""phash function from the github phash library for python"""
	img_size = hash_size * highfreq_factor
	image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
	pixels = np.asarray(image)
	dct = scipy.fftpack.dct(pixels)
	dctlowfreq = dct[:hash_size, 1:hash_size+1]
	avg = dctlowfreq.mean()
	diff = dctlowfreq > avg
	return diff

def convert_hash_to_int(hash_key):
    int = sum(2**i for i, v in enumerate(reversed(hash_key)) if v)
    return int

def convert_to_binary(list_of_true_and_falses):
    """convert true and false output of the phash function to a binary string"""
    new_list = [1 if x == True else 0 for x in list_of_true_and_falses]
    return new_list

def average_out_hashes(list_of_hashes):
    """turn a list of hashes into ints, take the average, and then return a new binary string"""
    list_of_ints = [convert_hash_to_int(old_hash) for old_hash in list_of_hashes]
    avg_int = int(sum(list_of_ints) / len(list_of_hashes))
    average_hash = bin(avg_int)
    return average_hash



def get_video_hash(path_film , hash_size = 8, high_freq_factor=4):
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

    average_hash = average_out_hashes(hashes)[2:]
    average_hash_simple = average_out_hashes(hashes_simple)[2:]
    new_hash = [int(x) for x in average_hash]
    new_hash_simple = [int(x) for x in average_hash_simple]
    return new_hash, new_hash_simple

def get_video_hashes(path_films, hash_size = 8, high_freq_factor = 4):
    new_hashes = []
    new_hashes_simple = []
    for path_film in path_films:
        new_hash, new_hash_simple = get_video_hash(path_film, hash_size, high_freq_factor)
        new_hashes.append(new_hash)
        new_hashes_simple.append(new_hash_simple)
    return new_hashes, new_hashes_simple

def get_video_hash_list(path_film, method = 'hash' ,hash_size = 8, high_freq_factor=4):
    """get a hash for each frame and then return a list of hashes"""
    counter = 0
    hashes = []
    hashes_simple = []
    filepathnamelist = glob.glob(path_film)
    filepathnamelist = sorted(filepathnamelist, key=lambda x: int(os.path.basename(x).split('.')[0].split('frame')[-1]))
    for filepathname in filepathnamelist:
        counter += 1
        im = Image.open(filepathname)
        if method == 'hash':
            hash = phash_own(im, hash_size, high_freq_factor)
        elif method == 'simple':
            hash = phash_simple_own(im, hash_size, high_freq_factor)
        else:
            raise ValueError("'Method' must be 'hash' or 'simple'")
        hash = convert_to_binary(hash.flatten())
        hashes.append(hash)

    return hashes, hashes_simple

def get_video_hash_list_stream(path_film, selection_frequency = 60, selection = 'total', chunksize = 5, method = 'hash' ,hash_size = 8, high_freq_factor=4):
    """get a hash for each frame and then return a list of hashes"""
    counter = 0
    hashes = []
    hashes_simple = []
    filepathnamelist_original = glob.glob(path_film)
    filepathnamelist_original = sorted(filepathnamelist_original)

    selection_index = int(len(filepathnamelist_original) / 2)
    if selection == 'first_half':
        filepathnamelist = filepathnamelist_original[:selection_index]
    elif selection == 'second_half':
        filepathnamelist = filepathnamelist_original[selection_index:]
    elif selection == 'total' or selection == 'chunks':
        filepathnamelist = filepathnamelist_original
    else:
        raise ValueError("'Selection' must be 'total', 'split', 'first_half' or 'second_half'")

    selection_filepathnamelist = []

    for filepathname in filepathnamelist:
        if counter == 0 or (counter % selection_frequency) == 0:
            print(filepathnamelist_original.index(filepathname), ' of ', len(filepathnamelist_original), ' :', os.path.basename(filepathname))
            im = Image.open(filepathname)
            if method == 'hash':
                hash = dhash(im, hash_size)
            elif method == 'simple':
                hash = phash_simple_own(im, hash_size, high_freq_factor)
            else:
                raise ValueError("'Method' must be 'hash' or 'simple'")
            hash = convert_to_binary(hash.flatten())
            hashes.append(hash)
            selection_filepathnamelist.append(filepathname)

        counter += 1

    if selection == 'chunks':
        selection_filepathnamelist = chunks(selection_filepathnamelist, chunksize)
        hashes = chunks(hashes, chunksize)

    return selection_filepathnamelist, hashes


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


def get_results_frame_by_frame(movie_hashes, movie_hashes_2 = None):
    if movie_hashes_2 != None:
        movie_hashes_2 = movie_hashes_2
        if len(movie_hashes) != len(movie_hashes_2):
            length = min(len(movie_hashes), len(movie_hashes_2))
            movie_hashes = movie_hashes[:length-1]
            movie_hashes_2 = movie_hashes[:length-1]
    else:
        movie_hashes_2 = movie_hashes

    from scipy.spatial.distance import cdist
    results = cdist(movie_hashes, movie_hashes_2, 'hamming')
    results = 1-results
    return results




def hamming_distance_2_hash_lists(hashlist1, hashlist2):
    """get the hamming distance between two list of hashes"""
    import numpy as np
    nr_of_frames = min(len(hashlist1), len(hashlist2))
    hamming_distances = []
    for i in range(0, nr_of_frames):
        hamming_distance = distance.hamming(hashlist1[i], hashlist2[1])
        hamming_distances.append(hamming_distance)
        # add, if next frame has smaller hamming distance, skip the previous frame (gridsearch
    hamming_distances = np.array(hamming_distances)
    indexes_of_low_distances, = np.where(hamming_distances < 0.2)
    perc_of_low_distances = float(len(indexes_of_low_distances) / nr_of_frames)
    print('perc_of_low_distances: {:.2f} %'.format(perc_of_low_distances))
    print(hamming_distances)
    print('mean ', np.mean(hamming_distances))
    #print('sum ', np.sum(hamming_distances), 'length = {hoi:d}'.format(hoi = nr_of_frames)) #naam/index: 5.3f
    print('std ', np.std(hamming_distances))
    print('min ', np.min(hamming_distances))
    print('max ', np.max(hamming_distances))
    return hamming_distances
