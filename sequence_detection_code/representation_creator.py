import abc
import cv2
from collections import deque


class RepresentationCreator(abc.ABC):

    def __init__(self, window_size, merge_function=None):
        self.window_size = window_size
        self.queue = deque(maxlen=window_size)
        self.merger = merge_function

    def next_frame(self, frame_path, timestamp):
        if len(self.queue) > 0 and self.queue[0][1] >= timestamp:
            raise ValueError("Timestamp ({}) must be increasing".format(timestamp))
        frame = cv2.imread(frame_path, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Frame ('{}') could not be loaded".format(frame_path))
        self.queue.append((frame, timestamp))

    def get_start_frame(self):
        return self.get_start()[0]

    def get_end_frame(self):
        return self.get_end()[0]

    def get_start(self):
        return self.queue[len(self.queue)]

    def get_end(self):
        return self.queue[0]

    def get_frames(self):
        return [item[0] for item in self.queue]

    @abc.abstractmethod
    def __create_representation__(self, frame):
        pass

    def create_representation(self):
        reps = []
        for frame in self.get_frames():
            representation = self.__create_representation__(frame)
            reps.append(representation)
        return self.merger.merge(*reps)

    def reset(self):
        self.queue.clear()
