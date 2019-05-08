
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