from comparison import Comparator
from merger import AverageMergeStrategy
from representations import hash_methods
import distance
import time
import plot
from representations.VGG16 import VGG16RepresentationCreator
from representations.googlenet import GoogLeNetRepresentationCreator
from representations.histogram import HistogramRepresentationCreator


one_dir = "/home/emma/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/test/"
other_dir = "/home/emma/Documenten/Media Distillery/replay-recognition/voorbeeld-data/journaal/test1/"

window_size = 1

run_name = 'pHash'
print(run_name)
timestamp = int(time.time())
print(timestamp)
rep_creator = hash_methods.HashRepresentationCreator(window_size, hash_methods.phash, hash_methods.default_params)
rep_creator.merger = AverageMergeStrategy()
distance_calculator = distance.HammingDistanceCalculator()
plotter = plot.Plot(window_size, run_name)
    comparator = Comparator(rep_creator, distance_calculator, plotter)
    dist = comparator.run_comparison(one_dir, other_dir)

run_name = 'Histogram'
print(run_name)
timestamp = int(time.time())
print(timestamp)
rep_creator = HistogramRepresentationCreator(window_size, 256)
rep_creator.merger = AverageMergeStrategy()
distance_calculator = distance.CosineDistanceCalculator()
plotter = plot.Plot(window_size, run_name)
comparator = Comparator(rep_creator, distance_calculator, plotter)
dist = comparator.run_comparison(one_dir, other_dir)


run_name = 'GoogleNet'
print(run_name)
timestamp = int(time.time())
print(timestamp)
rep_creator = GoogLeNetRepresentationCreator(window_size)
rep_creator.merger = AverageMergeStrategy()
distance_calculator = distance.CosineDistanceCalculator()
plotter = plot.Plot(window_size, run_name)
comparator = Comparator(rep_creator, distance_calculator, plotter)
dist = comparator.run_comparison(one_dir, other_dir)


run_name = 'VGG'
print(run_name)
timestamp = int(time.time())
print(timestamp)
rep_creator = VGG16RepresentationCreator(window_size)
rep_creator.merger = AverageMergeStrategy()
distance_calculator = distance.CosineDistanceCalculator()
plotter = plot.Plot(window_size, run_name)
comparator = Comparator(rep_creator, distance_calculator, plotter)
dist = comparator.run_comparison(one_dir, other_dir)

