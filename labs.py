from json import load as get_json
from interface import *
import algo
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


def run_algo(algo_name):
    try:
        data = get_data()
        _locals = locals()
        if not data:
            print("\033[31mError: incorrect parameter\033[0m")
            return
        exec(algo.algo_run[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + str(algo_result))
        save_data(algo_result)
    except ValueError as err:
        print(err)
        print("\033[31mError: incorrect parameter type\033[0m")


def hack_smth():
    data = get_data()
    _locals = locals()
    if not data:
        print("\033[31mError: incorrect parameter\033[0m")
        return
    method = input('?>> Enter algo: ')
    command_str = "algo_result = algo.hack_" + method + '(data)'
    try:
        exec(command_str, globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + str(algo_result))
        save_data(algo_result)
    except AttributeError as a:
        print(a)
        print("\033[31mError: incorrect algo\033[0m")
    except FileNotFoundError:
        print("\033[31mError: File not found\033[0m")
    except ValueError as err:
        print(err)
        print("\033[31mError: Failed!!!\033[0m")


def get_actions():
    with open("actions.json") as jfile:
        return get_json(jfile)


def main_loop(commands_list):
    while(True):
        command = input('#>> ')
        if command == "":
            continue
        try:
            exec(commands_list[command])
        except KeyError as err:
            print(err)
            print("\033[31mError: incorrect command\033[0m")


if __name__ == "__main__":
    commands_list = get_actions()
    draw_header()
    main_loop(commands_list)
