"""Load the average SNRs for every audio signal. Compute the weighted average of the SNRs using the number of componnets as the weights.

Plot the average SNRs
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








def savefigure(title, xlabel, ylabel, Y, labels, x, path_save_dir, type = "linear"):
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
    plt.ylim((0,16))
    if len(Y) != len(labels):
        print("Number of labels and plots don't match!")
        return

    for i in range(len(Y)):
        y = Y[i]
        if type == "linear":
            plt.plot(x, y, label = labels[i])
        elif type == "semilogx":
            plt.semilogx(x, y, label = labels[i])
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
















windows = ["Hann", "Hamming", "Blackman harris"]


path_averages = "../../experiments/experiment3/largescale/averages"
path_num_componnets = "../../experiments/experiment3/largescale/averages/num_components.txt"

with open(path_num_componnets, "r") as handle:
	num_sources_info = handle.read()

audios_info = num_sources_info.strip().split("\n")
audios_info_dict = {}
for audio in audios_info:
	name = audio.strip().split(" ")[0]
	num_comps = audio.strip().split(" ")[1]
	audios_info_dict[name] = int(num_comps)

print(audios_info_dict)


average_files = [file for file in listdir(path_averages) if file.endswith(".pickle")]
print(average_files)


# iterate over files
# obtain window details for each file
# multiply by the number of original sources present
# append to the window list
# sum over the final list along axis 0
# divide by the total number of original components

hamming = []
hann = []
blackmanharris = []
total_num_sources = 0

for file in average_files:
	audio_name = file.split("_")[0]
	print(audio_name)
	num_sources = audios_info_dict[audio_name]
	total_num_sources = total_num_sources + num_sources
	path_info = join(path_averages, file)
	with open(path_info, "rb") as handle:
		file_info = pickle.load(handle)
		hamming.append(num_sources*np.array(file_info["Hamming"][1]))
		hann.append(num_sources*np.array(file_info["Hann"][1]))
		blackmanharris.append(num_sources*np.array(file_info["Blackman harris"][1]))
		R = file_info["Hamming"][0]
	print("num sources", num_sources)

hamming = np.array(hamming)
hann = np.array(hann)
blackmanharris = np.array(blackmanharris)

print(np.shape(hamming))
print(np.shape(hann))
print(np.shape(blackmanharris))
print(total_num_sources)

hamming = np.sum(hamming, axis = 0)/ total_num_sources
hann = np.sum(hann, axis = 0)/ total_num_sources
blackmanharris = np.sum(blackmanharris, axis = 0)/ total_num_sources

print(np.shape(hamming))
print(np.shape(hann))
print(np.shape(blackmanharris))

Y = [hann, hamming, blackmanharris]
labels = ["Hann", "Hamming", "Blackman Harris"]
print(R)

savefigure("Variance_of_SNR_with_windows", "frame size" , "average snr over sources and components", Y, labels, R, path_averages)
# for file in average_files:
# 	with open(file, "rb") as handle:
# 		file_info = pickle.load(handle)
# 		for key in file_info:
# 			print(key)
# 			print(audios_info)

