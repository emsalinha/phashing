import abc
import numpy as np
from scipy.spatial import distance
from scipy.spatial.distance import cdist
from typing import List


class DistanceCalculator(abc.ABC):

    def calculate_distance(self, one: np.ndarray, other: np.ndarray) -> float:
        pass

    def calculate_distances(self, one_list: np.ndarray, other_list: np.ndarray) -> np.ndarray:
        distances = np.zeros((len(one_list), len(other_list)))
        for i, one_val in enumerate(one_list):
            for j, other_val in enumerate(other_list):
                dist = self.calculate_distance(one_val, other_val)
                distances[i, j] = dist
        return distances

    def calculate_distances_cdist(self, one_list: List[np.ndarray], other_list: List[np.ndarray]) -> np.ndarray:
        pass


class EuclideanDistanceCalculator(DistanceCalculator):

    def calculate_distance(self, one, other):
        return 1-distance.euclidean(one, other)

    def calculate_distances_cdist(self, one: List[np.ndarray], other: List[np.ndarray]):
        similarness = cdist(np.array(one), np.array(other), metric='euclidean')
        dist = 1-similarness
        return dist


class CosineDistanceCalculator(DistanceCalculator):

    def calculate_distance(self, one, other):
        return 1-distance.cosine(one, other)

    def calculate_distances_cdist(self, one: List[np.ndarray], other: List[np.ndarray]):
        similarness = cdist(np.array(one), np.array(other), metric='cosine')
        dist = 1-similarness
        return dist


class HammingDistanceCalculator(DistanceCalculator):

    def calculate_distance(self, one, other):
        return 1-distance.hamming(one, other)

    def calculate_distances_cdist(self, one: List[np.ndarray], other: List[np.ndarray]):
        similarness = cdist(np.array(one), np.array(other), metric='hamming')
        dist = 1-similarness
        return dist
