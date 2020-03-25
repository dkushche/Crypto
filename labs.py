import crypto_tools
import algo
import hack
import os


def get_data():
    data = crypto_tools.crypto_term("input", "Enter cyphered data or $filename.crypt: ", "ans")
    if ".crypt" in data:
        return crypto_tools.download_text("storage/" + data)
    return data


def save_data(algo_result):
    filename = crypto_tools.crypto_term("input", "Save to file?($filename/no): ", "ans")
    if filename == "no":
        crypto_tools.crypto_term("output", "OK, without saving", "inf")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        crypto_tools.save_text("storage/" + filename + ".crypt", algo_result)
        crypto_tools.crypto_term("output", "Saved in storage/" + filename + ".crypt", "inf")


def run_algo(algo_name):
    try:
        data = get_data()
        _locals = locals()
        if not data:
            crypto_tools.crypto_term("output", "Error: incorrect parameter", "err")
            return
        exec(algos[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        crypto_tools.crypto_term("output", "Result: " + str(algo_result), "inf")
        save_data(algo_result)
    except ValueError as err:
        crypto_tools.crypto_term("output", err, "err")
        crypto_tools.crypto_term("output", "Error: incorrect parameter type", "err")


def main_loop():
    while(True):
        command = crypto_tools.crypto_term("input", "", "def")
        if command == "":
            continue
        try:
            exec(commands_list[command])
        except KeyError as err:
            crypto_tools.crypto_term("output", err, "err")
            crypto_tools.crypto_term("output", "Error: incorrect command", "err")


if __name__ == "__main__":
    try:
        commands_list = crypto_tools.download_json("actions.json")
        algos = crypto_tools.download_json("algo_run.json")
    except FileNotFoundError:
        exit()
    crypto_tools.render_static('header')
    main_loop()
