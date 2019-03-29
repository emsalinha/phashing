import os
import numpy as np

path_move_to = '/home/emsala/Documenten/Media Distillery/replay-recognition/adbreak-dataset/compare_programs'
path = '/home/emsala/Documenten/Media Distillery/replay-recognition/adbreak-dataset'

title_program_dictionary = np.load('{}/program_dict.npy'.format(path)).item()

for title, programs in title_program_dictionary.items():
    os.mkdir(path_move_to + '/{}/'.format(title))

    for program in programs:
        program_id = program[0]
        try:
            os.mkdir(path_move_to + '/{}/{}'.format(title, program_id))
        except:
            continue
