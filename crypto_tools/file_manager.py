from json import load as get_json
from .gen_tools import utf_decoder


def get_param_json_data(fname, param):
    result = download_json("algo_storage/" + fname)
    if param not in result:
        raise ValueError("Incorrect param {0}".format(param))
    result = result[param]
    return result


def download_json(name):
    try:
        with open(name) as algo:
            return get_json(algo)
    except FileNotFoundError:
        raise


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
