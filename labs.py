from json import load as get_json
from interface import *
import algo

def hack_smth():
    _locals = locals()
    data = input('?>> Enter cyphered data: ')
    method = input('?>> Enter algo: ')
    command_str = "algo_result = algo.hack_" + method + "('" + data + "')"
    try:
        exec(command_str, globals(), _locals)
        algo_result = _locals['algo_result']
        print(algo_result)
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