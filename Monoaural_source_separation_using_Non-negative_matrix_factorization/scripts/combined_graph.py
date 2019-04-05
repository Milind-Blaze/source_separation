import argparse
import os
from os import listdir
from os.path import join
import pickle
import sys

import librosa
import librosa.display
from librosa.core import resample
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import scipy
from scipy.io.wavfile import write
from sklearn.decomposition import NMF

# relative imports as the directory structure is
# blah-blah/source_separation/examples,
# blah-blah/source_separation/nmf,
# TODO: (0) find a more scalable way for this
sys.path.insert(0,"../../../source_separation/")
from sourcesep.sourcesep import *
from tools.basic_functions import *


def obtain_variables_from_pickle(path_pickle):
	"""read the stored variables from the pickle file

	Parameters:
		path_pickle (string): path to the pickle file
	Returns: 
		Y (list): list of plots for a given experiment
		labels (list ): labels for each graph
		R (list): range of epochs

		
	"""
	with open(path_pickle, "rb") as handle:
		results = pickle.load(handle)
	Y = results["Y"]
	labels = results["labels"]
	R = results["R"]
	if type(R) != list:
		print("creating R due to original error")
		R = np.arange(R - len(Y[0]), R, 1)
	return Y, labels, R



path_experiment3_40ms = "../experiments/experiment3/alpha_10_beta_0.1_numcomp_40_40ms/Experiment3_10_1_0.04.pickle"
# path_experiment3_40ms = "../experiments/experiment3/temp/Experiment3_10_1_0.04.pickle"


with open(path_experiment3_40ms, "rb") as handle:
	results = pickle.load(handle)


Y = results["Y"]
labels = results["labels"]
R = results["R"]
if type(R) != list:
	print("creating R due to original error")
	R = np.arange(R - len(Y[0]), R, 1)

savefigure("Experiment3_SNR_windows", "Number of components", "Average SNR over all sources", Y, labels, R,"../experiments/experiment3/combined_stuff")