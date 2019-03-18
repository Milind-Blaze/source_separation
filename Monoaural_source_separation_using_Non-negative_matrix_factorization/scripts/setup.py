
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

############################################### Functions ##################################################

def savefigure(title, xlabel, ylabel, Y, labels, x, path_save_dir):
	"""
	Function to create and save plots

	Parameters:
		title (string): title of the plot
		xlabel (string): label of the x axis of the plot
		ylabel (string): label of the y axis of the plot
		Y (list): list of all the functions to be plotted on the Y axis
		labels (list): list of plot names for the legend
		x (array): array of the x axis values
		path_save_fig (string): folder where the plot must be saved

	"""
	plt.figure(figsize = (10,8))
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid(True)

	if len(Y) != len(labels):
		print("Number of labels and plots don't match!")
		return

	for i in range(len(Y)):
		y = Y[i]
		plt.plot(x,y, label = labels[i])
	plt.legend()
	try:
		os.mkdir(path_save_dir)
		print("folder created at " + path_save_dir)
	except FileExistsError:
		print("folder already exists at " + path_save_dir)
	path_save_fig = join(path_save_dir, title + ".png")
	plt.savefig(path_save_fig)
	print(title + ".png saved at " + path_save_fig)
	plt.close()

	return


############################################### Setting the variables including defaults ##################################################


figsize = (10,8)
matplotlib.rcParams.update({'font.size': 22})
fs_target = 44100


# audio input, separated sources, directory to store the final images in, r, beta, alpha
parser = argparse.ArgumentParser()
parser.add_argument("folder", help = "folder containing the mixture and the separated components")
parser.add_argument("audio", help = "name of the audio being separated")
parser.add_argument("expt_dir", help = "folder to store the plots generated, separated components and results of separation")
parser.add_argument("r", help = "number of components", type = int)
parser.add_argument("alpha", help = "scaling of the temporal continuity cost", type = float)
parser.add_argument("beta", help = "scaling of the sparseness cost", type = float)
parser.add_argument("--numiter", default = 1000, help = "number of iterations of the update algorithm to run", type = int)
parser.add_argument("--frame_size", default = 40e-3, help = "frame size in seconds", type = float)
parser.add_argument("--overlap", default = 0.5, help = "fraction of overlap between successive frames", type = float)
parser.add_argument("--window", default = "hann", help = "window to be used when extracting the stft")
args = parser.parse_args()


path_material = args.folder
path_expt_dir = args.expt_dir
audio_name = args.audio
r = args.r
alpha = args.alpha
beta = args.beta
numiter = args.numiter
frame_size = args.frame_size
overlap = args.overlap

n_fft = int(frame_size*fs_target) # datatype is an advantage for future use
hop_length = int((1-overlap)*frame_size*fs_target)

if args.window == "hann":
	window = scipy.signal.hann(n_fft)
# TODO: (0) add hamming and the others he was talking about


print("n_fft: ", n_fft)
print("hop_length: ", hop_length)
print("\n")

############################################### loading the audio ##################################################

path_audio = join(path_material, audio_name + ".wav")
audio, fs, t = load_audio(fs_target, path_audio)
savefigure(audio_name, "time", "audio", [audio], [audio_name], t, path_expt_dir)
audio_spec = librosa.core.stft(audio, n_fft = n_fft, hop_length = hop_length, window = window, center= True)
audio_spec_mag = np.abs(audio_spec)
audio_spec_phase = np.angle(audio_spec)
print("\n")
############################################### loading the separated components ##################################################

audio_number = audio_name[-1]
sepstart = "separated" + audio_number
sepname = [name for name in listdir(path_material) if name.startswith(sepstart)]
seppaths = [join(path_material, name) for name in sepname]
print("number of separated components found: ",len(seppaths))

sepmags = []
sepphases = []
for i in range(len(seppaths)):
	seppath = seppaths[i]
	sepsource, _, _ = load_audio(fs_target, seppath)
	if len(sepsource) != len(audio):
		sepsource = np.pad(sepsource, (0, len(audio) - len(sepsource)), "constant", constant_values = (0,0))
	sepspec = librosa.core.stft(sepsource, n_fft = n_fft, hop_length = hop_length, window = window, center = True)
	sepmag = np.abs(sepspec)
	sepphase = np.angle(sepspec)
	sepmags.append(sepmag)
	sepphases.append(sepphase)
	savefigure(sepname[i], "time", "audio", [sepsource], [sepname[i]], t, path_expt_dir)

print("\n")




############################################### creating a readme  ##################################################

path_readme = join(path_expt_dir, "readme.txt")
f = open(path_readme, "w")
f.write("Experiment file: " + sys.argv[0] + "\n")
f.write("Audio file being separated: " +  audio_name + "\n")
f.write("r (use varies, can be upper limit on or exactly the number of components): " + str(r) + "\n")
f.write("alpha: " + str(alpha) + "\n")
f.write("beta: " + str(beta) + "\n")
f.write("numiter: " + str(numiter) + "\n")
f.write("frame_size: " + str(frame_size) + "\n")
f.write("overlap: " + str(overlap) + "\n")
f.write("window: "+ args.window + "\n")
f.write
f.close() 
