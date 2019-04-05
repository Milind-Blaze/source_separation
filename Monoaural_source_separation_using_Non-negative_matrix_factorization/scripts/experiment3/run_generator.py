"""Generates the run.sh file required for experiment 3 - the computation of average snr part
"""

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
sys.path.insert(0,"../../../../source_separation/")
from sourcesep.sourcesep import *
from tools.basic_functions import *


base = "python experiment3.py ../../audios/orig4/ orig4 ../../experiments/experiment3/largescale/"
alpha = 10
beta = 0.1
num_comps = 40
num_iter = 1000
framesizes = np.arange(30,100,3)


filename = "run_expt3_combined.sh"
file2 = open(filename, "w+")


for framesize in framesizes:
	foldername = "alpha_" + str(alpha) + "_beta_" + str(beta) + "_numcomp_" + str(num_comps) + "_windows_" + str(framesize) + "ms/"
	values = " " + str(num_comps) + " " + str(alpha) + " " + str(beta) + " " +  "--numiter " + str(num_iter)
	frames = " --frame_size " + str(framesize) + "e-3"
	command = base + foldername + values + frames + "\n"
	file2.write(command)


print("Done!")
file2.close()