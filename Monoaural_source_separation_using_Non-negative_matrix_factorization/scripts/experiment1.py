# TODO: (10) Docstring goes here

import argparse
import os
from os import listdir
from os.path import join
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
from setup import *

############################################### varying r ##################################################

# The paper varies r from len(seppaths) to 30. Therefore, here too, r shall be varied from 7 to 30 n

R = np.arange(len(seppaths), 30, 1)


############################################### NMF EUL ##################################################

for r in range 