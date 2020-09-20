from .file_manager import download_text, save_text
from .interface import cterm
import functools
import time
import os


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


def file_manipulation(function):
    @functools.wraps(function)
    def wrapper_filesystem(*args, **kwargs):
        try:
            data = get_data()
            if not data:
                raise ValueError
            result = function(data, *args, **kwargs)
            cterm("output", "Result: " + str(result), "inf")
            save_data(result)
        except ValueError as err:
            cterm("output", err, "err")
            cterm("output", "Error: incorrect parameter type", "err")
    return wrapper_filesystem


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
