import crypto_tools
import algo
import hack


def run_algo(algo_name):
    try:
        data = crypto_tools.get_data()
        _locals = locals()
        if not data:
            print("\033[31mError: incorrect parameter\033[0m")
            return
        exec(algos[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        print("Result: " + str(algo_result))
        crypto_tools.save_data(algo_result)
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
    try:
        commands_list = crypto_tools.download_json("actions.json")
        algos = crypto_tools.download_json("algo_run.json")
    except FileNotFoundError:
        exit()
    crypto_tools.render_static('header')
    main_loop()
