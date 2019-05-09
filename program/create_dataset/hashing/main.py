import glob
import os
import time
import argparse
from create_dataset.hashing.phash import phash














if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--VM', type=bool, default=False, help='Running on VM or not')
	config = parser.parse_args()
	extract_frames(config)
