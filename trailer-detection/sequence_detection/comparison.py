import logging
from os import walk, path


class Comparator(object):

    def __init__(self, representation_creator, distances_calculator, plot_creator):
        self.rep_creator = representation_creator
        self.distances_calc = distances_calculator
        self.plotter = plot_creator
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_comparison(self, one_dir_path, other_dir_path):
        one_embedding_list, one_ordered_files_paths = self._load_embeddings(one_dir_path)
        other_embedding_list, other_ordered_files_paths = self._load_embeddings(other_dir_path)
        distances = self.distances_calc.calculate_distances_cdist(one_embedding_list, other_embedding_list)
        self._plot(distances, one_ordered_files_paths, other_ordered_files_paths)
        return distances

    def _load_embeddings(self, dir_path):
        representations = []
        self.rep_creator.reset()
        ordered_files_paths = self._get_files(dir_path)
        for i, file_path in enumerate(ordered_files_paths):
            self.rep_creator.next_frame(file_path, i)
            representation = self.rep_creator.create_representation()
            representations.append(representation)
        return representations, ordered_files_paths

    def _plot(self, distances, one_ordered_files_paths, other_ordered_files_paths):
        self.plotter.plot(distances, one_ordered_files_paths, other_ordered_files_paths)

    @staticmethod
    def _get_files(dir_path):
        ordered_files_paths = []
        for _, _, files in walk(dir_path):
            files = [file for file in files if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')]
            sorted_files = sorted(files)
            for file in sorted_files:
                ordered_files_paths.append(path.join(dir_path, file))
        return ordered_files_paths
