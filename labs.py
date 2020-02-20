from file_manager import get_data, save_data, download_conf
from interface import draw_header, print_help
import algo
import hack


def run_algo(algo_name):
    try:
        data = get_data()
        _locals = locals()
        if not data:
            print("\033[31mError: incorrect parameter\033[0m")
            return
        exec(algos[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + str(algo_result))
        save_data(algo_result)
    except ValueError as err:
        print(err)
        print("\033[31mError: incorrect parameter type\033[0m")


def main_loop():
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
    commands_list = download_conf("actions.json")
    algos = download_conf("algo_run.json")
    draw_header()
    main_loop()
