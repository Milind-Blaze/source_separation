"""Experiment 2: Variation of SNR with alpha and beta

Vary alpha while keeping beta zero and vice versa. Plot SNR vs alpha/ beta. 

Minimizes only virtanen loss. 

Requires argparse, os, librosa, matplotlib, numpy, scipy, scikit learn and the sourcesep.py file, tools.py file and setup.py file

Saves a plot of the SNRs with the algorithms vs alpha and beta at path_expt_dir provided on command line
"""


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
import setup


############################################### local variables ##################################################

numiter = setup.numiter
audio_spec = setup.audio_spec
audio_spec_mag = setup.audio_spec_mag
audio_spec_phase = setup.audio_spec_phase
sepmags = setup.sepmags
sepphases = setup.sepphases
r = setup.r

# number of points to take on the logarithmic alpha axis
num_alphas = 50 
# treats the alpha supplied as the lower bound of alphas/betas
# treats the beta supplied as the upper bound of alphas/betas
alphas = np.logspace(np.log10(setup.alpha), np.log10(setup.beta), num = num_alphas)
betas = alphas 

############################################### Alpha ##################################################

print("Multiple component allocation")
print("Virtanen loss")
print("Variation with alpha")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that i.e use multiple sources
snrs_over_alpha = []
for alpha in alphas:
	print("alpha: " + str(alpha))
	snrs_for_alpha = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, alpha, 0, numiter, toprint= None)
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
				# magnitude spec(reconstructed source) = sum(magnitude spec(reconstruced components allocated to each source))
				recon_source_mag = recon_source_mag + allocation[l][comp]
			snr_lth_source = SNR(allocation[l][0], recon_source_mag)
			snrs_for_alpha.append(snr_lth_source)

	snrs_for_alpha = np.array(snrs_for_alpha)
	log_snrs_for_alpha = 10*np.log10(snrs_for_alpha)
	avg_snr_alpha = np.mean(log_snrs_for_alpha)
	snrs_over_alpha.append(avg_snr_alpha)
	print("Number of undetected sources: " + str(undetected))
	print("Average SNR over all sources: " + str(avg_snr_alpha))



savefigure("Experiment 2a: SNR variation with alpha, beta = 0", "alpha", "Average SNR over all sources", [snrs_over_alpha], 
	["variation with alpha"], alphas, setup.path_expt_dir, type = "semilogx")


############################################### Beta variation ##################################################

print("Multiple component allocation")
print("Virtanen loss")
print("Variation with beta")
# This is average over one mixture, not over multiple mixtures, TODO: (0) remedy that i.e use multiple sources
# LAZY CODING: swapping alpha and zero in the virtanen007_find function serves the purpose
snrs_over_alpha = []
for alpha in alphas:
	print("beta: " + str(alpha))
	snrs_for_alpha = []
	# separate the components
	B, G, _ = virtanen007_find(audio_spec_mag, r, 0, alpha, numiter, toprint= None)
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
				# magnitude spec(reconstructed source) = sum(magnitude spec(reconstruced components allocated to each source))
				recon_source_mag = recon_source_mag + allocation[l][comp]
			snr_lth_source = SNR(allocation[l][0], recon_source_mag)
			snrs_for_alpha.append(snr_lth_source)

	snrs_for_alpha = np.array(snrs_for_alpha)
	log_snrs_for_alpha = 10*np.log10(snrs_for_alpha)
	avg_snr_alpha = np.mean(log_snrs_for_alpha)
	snrs_over_alpha.append(avg_snr_alpha)
	print("Number of undetected sources: " + str(undetected))
	print("Average SNR over all sources: " + str(avg_snr_alpha))



savefigure("Experiment 2b: SNR variation with beta, alpha = 0", "beta", "Average SNR over all sources", [snrs_over_alpha], 
	["variation with beta"], alphas, setup.path_expt_dir, type = "semilogx")
