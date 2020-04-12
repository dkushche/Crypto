import crypto_tools
import readline
import algo
import hack
import os


def completer(text, state):
    if completer.in_menu:
        options = [i for i in commands_list.keys() if i.startswith(text)]
        return options[state]
    return None


completer.in_menu = True


def get_data():
    sentence = "Enter cyphered data or $filename.crypt: "
    data = crypto_tools.cterm("input", sentence, "ans")
    if ".crypt" in data:
        return crypto_tools.download_text("storage/" + data)
    return data


def save_data(algo_result):
    sentence = "Save to file?($filename/no): "
    filename = crypto_tools.cterm("input", sentence, "ans")
    if not filename or filename == "no":
        crypto_tools.cterm("output", "OK, without saving", "inf")
    else:
        if not os.path.exists("storage/"):
            os.mkdir("storage/")
        crypto_tools.save_text("storage/" + filename + ".crypt", algo_result)
        sentence = "Saved in storage/" + filename + ".crypt"
        crypto_tools.cterm("output", sentence, "inf")


def run_algo(algo_name):
    try:
        data = get_data()
        _locals = locals()
        if not data:
            crypto_tools.cterm("output", "Error: incorrect parameter", "err")
            return
        exec(algos[algo_name], globals(), _locals)
        algo_result = _locals['algo_result']
        crypto_tools.cterm("output", "Result: " + str(algo_result), "inf")
        save_data(algo_result)
    except ValueError as err:
        crypto_tools.cterm("output", err, "err")
        crypto_tools.cterm("output", "Error: incorrect parameter type", "err")


def main_loop():
    while(True):
        command = crypto_tools.cterm("input", "", "def")
        if command == "":
            continue
        try:
            completer.in_menu = False
            exec(commands_list[command])
        except KeyError as err:
            crypto_tools.cterm("output", err, "err")
            crypto_tools.cterm("output", "Error: incorrect command", "err")
        completer.in_menu = True


if __name__ == "__main__":
    try:
        commands_file = "crypto_commands/actions.json"
        commands_list = crypto_tools.download_json(commands_file)
        algos = crypto_tools.download_json("crypto_commands/algo_run.json")
    except FileNotFoundError:
        exit()
    crypto_tools.render_static('header')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    readline.set_auto_history(False)
    main_loop()
