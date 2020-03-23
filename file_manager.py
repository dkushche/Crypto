from json import load as get_json
from crypto_tools import utf_decoder
import os


def get_data():
    data = input('?>> Enter cyphered data or $filename.crypt: ')
    if ".crypt" in data:
        return download_text("storage/" + data)
    return None


def save_data(algo_result):
    filename = input("Save to file?($filename/no): ")
    if filename == "no":
        print("OK, without saving")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        with open("storage/" + filename + ".crypt", 'wb') as f:
            if algo_result.__class__ == str:
                algo_result = bytearray(algo_result, "utf-8")
            f.write(algo_result)
        print("!>> Saved in storage/" + filename + ".crypt")


def download_conf(name):
    try:
        with open(name) as algo:
            return get_json(algo)
    except FileNotFoundError:
        print("\033[31mError: no {0} in algo package\033[0m".format(name))
        exit()


def download_text(name):
    try:
        with open(name, "rb") as text_file:
            return text_file.read()
    except FileNotFoundError:
        print("\033[31mError: {" + name + "} No such file\033[0m")
        return None


def render_static(file):
    header = download_text("iface_storage/crypto." + file)
    if header:
        header = "\033[36m" + utf_decoder(header) + "\033[0m"
    else:
        header = "\033[36mYou may add custom in crypto" + file + " file\033[0m"
    print(header)
