from json import load as get_json
import os


def get_data():
    data = input('?>> Enter cyphered data or $filename.crypt: ')
    if ".crypt" in data:
        try:
            with open("storage/" + data, "rb") as crypt_file:
                data = crypt_file.read()
        except FileNotFoundError:
            print("\033[31mError: incorrect filename\033[0m")
            return None
    return data


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
