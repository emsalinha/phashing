import abc
import logging
import numpy as np


class MergeStrategy(abc.ABC):

    @abc.abstractmethod
    def merge(self, one, other):
        raise NotImplementedError()


class AverageMergeStrategy(MergeStrategy):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def merge(self, *vectors):
        return np.mean(vectors, axis=0)
