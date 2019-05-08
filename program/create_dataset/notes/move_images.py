import numpy as np
import shutil
from ground_truth.get_filenames_to_move import df_filenames_to_move

base_path = '/home/emsala/Documenten/Media Distillery/replay-recognition/adbreak-dataset'

path_move_to = base_path + '/compare_programs'

folder_names = ['2018-02-24', '2018-03-01', '2018-03-02', '2018-03-03', '2018-03-04']
paths_move_from = [base_path + '/{}'.format(folder_name) for folder_name in folder_names]


title_program_dictionary = np.load(base_path + '/program_dict.npy').item()

counter = 0
for title, programs in title_program_dictionary.items():
    for program_info in programs:
        program_id = program_info[0]
        rst = int(program_info[3])
        program_file_names = df_filenames_to_move[df_filenames_to_move['timestamps'] > rst]
        ret = int(program_info[4])
        program_file_names = program_file_names[program_file_names['timestamps'] < ret]
        program_file_names = program_file_names['filenames'].values
        if len(program_file_names) > 0:
            for program_file_name in program_file_names:
                path_to = path_move_to + '/{}/{}'.format(title, program_id)
                path_from = base_path + '/{}'.format(program_file_name)
                try:
                    shutil.move(path_from, path_to)
                    print('moved {}'.format(program_file_name))
                except:
                    print('foutmelding')
                    continue
