""" Experiment 1: SNR variation with the number of components

Varies number of components from number of sources present to 40 and plots the SNRs for three loss funcitons. NMF EUL, NMF LOG
and Virtanen loss. 

Requires argparse, os, librosa, matplotlib, numpy, scipy, scikit learn and the sourcesep.py file, tools.py file and setup.py file

Saves a plot of the SNRs with the algorithms vs number of components at path_expt_dir provided on command line
"""

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
sys.path.insert(0,"../../../../source_separation/")
from sourcesep.sourcesep import *
from tools.basic_functions import *
import setup


############################################### local variables ##################################################

numiter = setup.numiter
audio_spec = setup.audio_spec
audio_spec_mag = setup.audio_spec_mag
audio_spec_phase = setup.audio_spec_phase
sepmags = setup.sepmags
sepphases = setup.sepphases
rmax = setup.r

R = np.arange(len(setup.seppaths), rmax, 1)
Y = []
labels = ["NMF EUL", "NMF LOG", "Virtanen007 loss"]

############################################### NMF EUL ##################################################

print("Multiple component allocation")
print("NMF EUL")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = lstfind(audio_spec_mag, r, numiter)
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

# plt.figure(figsize = (15,7))
# plt.plot(R, snrs_over_r)
# plt.show()
# plt.close()


############################################### NMF LOG ##################################################

print("Multiple component allocation")
print("NMF LOG")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = divfind(audio_spec_mag, r, numiter)
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

############################################### Virtanen loss ##################################################

print("Multiple component allocation")
print("Virtanen loss")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that
snrs_over_r = []
for r in R:
	print("r: " + str(r))
	snrs_for_r = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, setup.alpha, setup.beta, setup.numiter, toprint= None)
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

setup.savefigure("Experiment 1: SNR with nubmer of components", "Number of components", "Average SNR over all sources", Y, labels, R, setup.path_expt_dir)


# TODO: (0) figure out a way to iterate over multiple sources
