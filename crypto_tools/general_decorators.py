""" General Decorators

Set of decorators which are super useful while creating
standard crypto module flow

"""

import os
import time
import functools

from .file_manager import download_text, save_text
from .interface import cterm


def get_data():
    sentence = "Enter cyphered data or $filename.crypt: "
    data = cterm("input", sentence, "ans")
    if ".crypt" in data:
        return download_text("storage/" + data)
    return data


def save_data(algo_result):
    sentence = "Save to file?($filename/no): "
    filename = cterm("input", sentence, "ans")
    if not filename or filename == "no":
        cterm("output", "OK, without saving", "inf")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        save_text("storage/" + filename + ".crypt", algo_result)
        sentence = "Saved in storage/" + filename + ".crypt"
        cterm("output", sentence, "inf")


def file_manipulation(read_data=True, save=True):
    def actual_file_manipulation(function):
        @functools.wraps(function)
        def wrapper_filesystem(*args, **kwargs):
            if read_data:
                data = get_data()
                if not data:
                    raise ValueError
                if data.__class__ == str:
                    data = bytearray(data.encode())
                result = function(data, *args, **kwargs)
            else:
                result = function(*args, **kwargs)
            cterm("output", "Result: " + str(result), "inf")
            if save:
                save_data(result)
        return wrapper_filesystem
    return actual_file_manipulation


def check_time(function):
    @functools.wraps(function)
    def wrapper_check_time(*args, **kwargs):
        start_time = time.process_time()
        result = function(*args, **kwargs)
        end_time = time.process_time()
        dtime = str(end_time - start_time)
        cterm("output", function.__name__ +
              " spent " + dtime + " seconds", "inf")
        return result
    return wrapper_check_time
