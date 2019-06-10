"""Experiment 3: variation of the SNR with the window function

Varies number of components from number of sources present to the r value supplied in the command line and plots the SNRs for Virtanen loss. 

Requires argparse, os, librosa, matplotlib, numpy, scipy, scikit learn and the sourcesep.py file, tools.py file and setup.py file

Saves a plot of the SNRs with the algorithms vs number of components at path_expt_dir provided on command line
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



def save_results(Y, labels, R, filename, path_expt_dir):
	"""pickles the data generated from the experiment

	Pickles the results of the experiment as a dictionary with the keys "Y", "labels"
	and "R"

	Parameters:
		Y (list): list of arrays each of which corresponds to a plot
		labels (list): list of labels corresponinng to each plot
		R (list): range of the number of components
		filename (string): name of the picle file
		path_expt_dir (string): path to folder where the pickle file is to be saved

	"""
	results = {"Y": Y,
				"labels": labels,
				"R": R}
	filepath = join(path_expt_dir, filename)
	with open(filepath, 'wb') as handle:
		pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL) 



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


# TODO: (0) add hamming and the others he was talking about


print("n_fft: ", n_fft)
print("hop_length: ", hop_length)
print("\n")

############################################### creating a readme  ##################################################
try:
	os.mkdir(path_expt_dir)
	print("folder created at " + path_expt_dir)
except FileExistsError:
	print("folder already exists at " + path_expt_dir)


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
f.write("window: "+ "hann, hamming, blackmanharris" + "\n")
f.write
f.close()

############################################### loading the audio ##################################################

path_audio = join(path_material, audio_name + ".wav")
audio, fs, t = load_audio(fs_target, path_audio)
savefigure(audio_name, "time", "audio", [audio], [audio_name], t, path_expt_dir)

audio_number = audio_name.replace("orig", "")
sepstart = "separated" + audio_number
sepname = [name for name in listdir(path_material) if name.startswith(sepstart)]
seppaths = [join(path_material, name) for name in sepname]
print("number of separated components found: ",len(seppaths))


print("\n")

############################################### local variables ##################################################

rmax = r
assert rmax >= len(seppaths)
R = np.arange(len(seppaths), rmax, 1)

Y = []
# modify labels depending on what you want to run
# TODO: (0) make this entirely dependent on command line
labels = ["Hann", "Hamming", "Blackman harris"]



# TODO: (0) Very brutal and no reuse of code between windows. Really needs to be fixed.



############################################### Hann window ##################################################

window = scipy.signal.hann(n_fft)

audio_spec = librosa.core.stft(audio, n_fft = n_fft, hop_length = hop_length, window = window, center= True)
audio_spec_mag = np.abs(audio_spec)
audio_spec_phase = np.angle(audio_spec)
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


print("Multiple component allocation")
print("Virtanen loss")

print("Hann window")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, alpha, beta, numiter, toprint= None)
	components = reconmag_r_components(B,G)
	allocation = virtanen007_cluster_all(sepmags, components)
	undetected = 0

	for l in range(len(allocation)):
		# no components detected
		if np.shape(allocation[l])[0] == 1:
			print("Source " + str(l) + " undetected")
			undetected = undetected + 1
		else:
			recon_source_mag = 0
			# computing the snrs between the orignial source and the reconstructed source
			# TODO: (0) fix this
			for comp in np.arange(1,len(allocation[l])):
				recon_source_mag = recon_source_mag + allocation[l][comp]
			snr_lth_source = SNR(allocation[l][0], recon_source_mag)
			snrs_for_r.append(snr_lth_source)

	snrs_for_r = np.array(snrs_for_r)
	log_snrs_for_r = 10*np.log10(snrs_for_r)
	avg_snr_r = np.mean(log_snrs_for_r)
	snrs_over_r.append(avg_snr_r)
	print("Number of undetected sources: " + str(undetected))
	print("Average SNR over all sources: " + str(avg_snr_r))

Y.append(snrs_over_r)
print("\n")

############################################### Hamming window ##################################################

print("Hamming window")

window = scipy.signal.hamming(n_fft)

audio_spec = librosa.core.stft(audio, n_fft = n_fft, hop_length = hop_length, window = window, center= True)
audio_spec_mag = np.abs(audio_spec)
audio_spec_phase = np.angle(audio_spec)
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
	# already done for hann window
	# savefigure(sepname[i], "time", "audio", [sepsource], [sepname[i]], t, path_expt_dir)

print("\n")


# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, alpha, beta, numiter, toprint= None)
	components = reconmag_r_components(B,G)
	allocation = virtanen007_cluster_all(sepmags, components)
	undetected = 0

	for l in range(len(allocation)):
		# no components detected
		if np.shape(allocation[l])[0] == 1:
			print("Source " + str(l) + " undetected")
			undetected = undetected + 1
		else:
			recon_source_mag = 0
			# computing the snrs between the orignial source and the reconstructed source
			# TODO: (0) fix this
			for comp in np.arange(1,len(allocation[l])):
				recon_source_mag = recon_source_mag + allocation[l][comp]
			snr_lth_source = SNR(allocation[l][0], recon_source_mag)
			snrs_for_r.append(snr_lth_source)

	snrs_for_r = np.array(snrs_for_r)
	log_snrs_for_r = 10*np.log10(snrs_for_r)
	avg_snr_r = np.mean(log_snrs_for_r)
	snrs_over_r.append(avg_snr_r)
	print("Number of undetected sources: " + str(undetected))
	print("Average SNR over all sources: " + str(avg_snr_r))

Y.append(snrs_over_r)
print("\n")



############################################### Blackman harris window ##################################################

print("Blackmanharris window")

window = scipy.signal.blackmanharris(n_fft)

audio_spec = librosa.core.stft(audio, n_fft = n_fft, hop_length = hop_length, window = window, center= True)
audio_spec_mag = np.abs(audio_spec)
audio_spec_phase = np.angle(audio_spec)
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
	# already done for hann window
	# savefigure(sepname[i], "time", "audio", [sepsource], [sepname[i]], t, path_expt_dir)

print("\n")


# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, alpha, beta, numiter, toprint= None)
	components = reconmag_r_components(B,G)
	allocation = virtanen007_cluster_all(sepmags, components)
	undetected = 0

	for l in range(len(allocation)):
		# no components detected
		if np.shape(allocation[l])[0] == 1:
			print("Source " + str(l) + " undetected")
			undetected = undetected + 1
		else:
			recon_source_mag = 0
			# computing the snrs between the orignial source and the reconstructed source
			# TODO: (0) fix this
			for comp in np.arange(1,len(allocation[l])):
				recon_source_mag = recon_source_mag + allocation[l][comp]
			snr_lth_source = SNR(allocation[l][0], recon_source_mag)
			snrs_for_r.append(snr_lth_source)

	snrs_for_r = np.array(snrs_for_r)
	log_snrs_for_r = 10*np.log10(snrs_for_r)
	avg_snr_r = np.mean(log_snrs_for_r)
	snrs_over_r.append(avg_snr_r)
	print("Number of undetected sources: " + str(undetected))
	print("Average SNR over all sources: " + str(avg_snr_r))

Y.append(snrs_over_r)
print("\n")


print(R)
savefigure("Experiment3_SNR_windows", "Number of components", "Average SNR over all sources", Y, labels, R, path_expt_dir)




filename = "Experiment3_" + str(alpha) + "_" + str(beta) + "_" + str(frame_size) + ".pickle"
save_results(Y, labels, R, filename, path_expt_dir)
