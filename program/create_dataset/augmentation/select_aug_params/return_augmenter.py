from imgaug import augmenters as iaa


def return_augmenter(parameter, method):
    if method == 'subtract':
        augmenter = iaa.Sequential([iaa.Add(parameter, True)])
    if method == 'add':
        augmenter = iaa.Sequential([iaa.Add(parameter, True)])
    if method == 'gauss_neg' or method == 'gauss_pos':
        augmenter = iaa.Sequential([iaa.AdditiveGaussianNoise(parameter, 1.5, True)])
    if method == 'compress':
        augmenter = iaa.Sequential([iaa.JpegCompression(parameter)])
    if method == 'subtract_hsv':
        augmenter = iaa.Sequential(iaa.AddToHueAndSaturation(parameter, True))
    if method == 'add_hsv':
        augmenter = iaa.Sequential(iaa.AddToHueAndSaturation(parameter, True))
    if method == 'contrast':
        augmenter = iaa.Sequential(iaa.GammaContrast(parameter, False))
    return augmenter

def return_param_range(method):
    if method == 'subtract':
        param_range = range(-255, 0, 5)
    if method == 'add':
        param_range = range(0, 255, 5)
    if method == 'gauss_neg':
        param_range = range(-255, 0)
    if method == 'gauss_pos':
        param_range = range(0, 255)
    if method == 'compress':
        param_range = range(8000, 10000, 10)
        param_range = [param/100 for param in param_range]
    if method == 'subtract_hsv':
        param_range = range(-255, 0, 1)
    if method == 'add_hsv':
        param_range = range(0, 255, 1)
    if method == 'contrast':
        param_range = range(1, 100)
        param_range = [param/10 for param in param_range]
    return param_range



# add_param_range = range(-150, 150, 5)
# gauss_param_range = range(-100, 100, 5)
# n_params = len(gauss_param_range)
# step_size = (10+10)/n_params
# gaus_sigma_range = range(-10, 10, step_size)
# compress_param_range = range(80, 99)
# add_hsv_param_range = range(-150, 150, 5)
# contrast_param_range = range(0.1, 0.9)

