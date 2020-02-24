import matplotlib.pyplot as plt
import os


def create_subplots(**kwargs):
    n_of_plots = len(kwargs)
    index = 1
    for key in kwargs:
        lists = kwargs[key].items()
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
    filename = input("Save plot to file?($filename/no): ")
    if filename == "no":
        print("OK, without saving")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        plt.savefig("storage/" + filename + ".png")
        print("!>> Saved in storage/" + filename + ".crypt")


"""
    create plot gets parameters like
    name_plot=dict_with_data, other_name_plot=...
"""


def create_plot(**kwargs):
    create_subplots(**kwargs)
    plt.subplots_adjust(hspace=0.5)
    save_plot()
