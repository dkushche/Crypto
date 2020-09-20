import matplotlib.pyplot as plt
from .interface import cterm
import os


def create_subplots(subplot_data):
    n_of_plots = len(subplot_data)
    index = 1
    for key, value in subplot_data.items():
        lists = value.items()
        x, y = list(zip(*lists))
        plt.subplot(n_of_plots, 1, index)
        plt.grid(True)
        plt.title(key)
        x = list(x)
        spec_sym = {' ': 'S', '.': 'P', '_': 'U'}
        for i in range(len(x)):
            if x[i] in spec_sym:
                x[i] = spec_sym[x[i]]
        plt.plot(x, y)
        index += 1


def save_plot():
    filename = cterm("input", "Save plot to file?($filename/no): ", "ans")
    if filename == "no":
        cterm("output", "OK, without saving", "inf")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        plt.savefig("storage/" + filename + ".png")
        cterm("output", "Saved in storage/" + filename + ".png", "inf")


"""
    create plot gets parameters like
    name_plot=dict_with_data, other_name_plot=...
"""


def create_plot(subplot_data):
    create_subplots(subplot_data)
    plt.subplots_adjust(hspace=0.5)
    save_plot()
