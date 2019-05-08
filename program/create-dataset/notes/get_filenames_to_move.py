import glob
import pandas as pd

base_path = '/home/emsala/Documenten/Media Distillery/replay-recognition/adbreak-dataset'

folder_names = ['2018-02-24', '2018-03-01', '2018-03-02', '2018-03-03', '2018-03-04']
paths_move_from = [base_path + '/{}'.format(folder_name) for folder_name in folder_names]
print(paths_move_from)

filenames_to_move = []
for path in paths_move_from:
    file_paths_to_move = glob.glob(path + '/*')
    file_names_part = ['/' + '/'.join(file_path_to_move.split('/')[-2:]) for file_path_to_move in file_paths_to_move]
    filenames_to_move += file_names_part
    filenames_to_move = sorted(filenames_to_move)

timestamps = [int(filename.split('/')[2].replace('.jpg', '')) for filename in filenames_to_move]
data = {
    'filenames': filenames_to_move,
    'timestamps': timestamps
}
df_filenames_to_move = pd.DataFrame.from_dict(data)

print(len(df_filenames_to_move))