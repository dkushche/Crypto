from json import load as get_json
from interface import *
import algo


def get_data():
    data = input('?>> Enter cyphered data or $filename.crypt: ')
    if ".crypt" in data:
        try:
            with open(data) as crypt_file:
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
        with open(filename + ".crypt", 'w') as f:
            f.write(algo_result)
        print("!>> Saved in " + filename + ".crypt")


def run_algo(algo_name):
    try:
        data = get_data()
        _locals = locals()
        if not data:
            return
        exec(algo.algo_run[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + algo_result)
        save_data(algo_result)
    except ValueError as err:
        print(err)
        print("\033[31mError: incorrect parameter type\033[0m")


def hack_smth():
    data = get_data()
    _locals = locals()
    if not data:
        return
    method = input('?>> Enter algo: ')
    command_str = "algo_result = algo.hack_" + method + '("""' + data + '""")'
    try:
        exec(command_str, globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + algo_result)
        save_data(algo_result)
    except AttributeError:
        print("\033[31mError: incorrect algo\033[0m")


def get_actions():
    with open("actions.json") as jfile:
        return get_json(jfile)


def main_loop(commands_list):
    while(True):
        command = input('#>> ')
        try:
            exec(commands_list[command])
        except KeyError:
            print("\033[31mError: incorrect command\033[0m")


if __name__ == "__main__":
    commands_list = get_actions()
    draw_header()
    main_loop(commands_list)
