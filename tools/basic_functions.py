import os
from os.path import join

from matplotlib import pyplot as plt
import numpy as np

def plotfigure(figsize,xlabel,ylabel,title,x,y=[],style="k-",graph="plot"):
    plt.figure(figsize=figsize)
    plt.grid(True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if len(y) == 0:
        plt.plot(x,style)
    else:
        if graph=="plot":
            plt.plot(x,y,style)
        if graph== "semilogx":
            plt.semilogx(x,y,style)
        if graph== "semilogy":
            plt.semilogy(x,y,style)
        if graph== "loglog":
            plt.loglog(x,y,style)
    plt.tight_layout()
    plt.show()
    plt.close()


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
