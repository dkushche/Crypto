""" File Manager

Set of tools for dealing with crypto files

"""

from json import load


def get_param_json_data(fname, param):
    result = download_json("crypto_storage/" + fname)
    if param not in result:
        raise ValueError(f"Incorrect param {param}")
    result = result[param]
    return result


def download_json(name):
    with open(name, encoding="utf-8") as algo:
        return load(algo)


def save_text(name, value):
    with open(name, 'wb') as f:
        if value.__class__ == str:
            value = bytearray(value, "utf-8")
        f.write(value)


def download_text(name):
    try:
        with open(name, "rb") as text_file:
            return text_file.read()
    except FileNotFoundError:
        return None
