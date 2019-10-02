import pickle


def read_params(method):
        loc = '/home/emsala/Documenten/Studie/These/phashing/program/create_dataset/augmentation/select_aug_params/'
        with open(loc + 'aug_params/{}_param_moments.pickle'.format(method), 'rb') as handle:
            param_moments = pickle.load(handle)

        return param_moments


if __name__ == '__main__':
    methods = ['add', 'gauss', 'compress', 'subtract_hsv', 'add_hsv', 'contrast', 'subtract']

    for method in methods:

        param_moments = read_params(method)
        for ssid, moments in param_moments.items():
            print('{} SSID {}: {}, {}'.format(method, ssid, moments[0], moments[1]))

