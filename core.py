import crypto_commands
import crypto_tools
import functools
import readline
import algo
import hack
import os


def completer(text, state):
    if completer.in_menu:
        options = [i for i in all_commands if i.startswith(text)]
        return options[state]
    return None


completer.in_menu = True


def main_loop():
    while True:
        command = None
        command_name = crypto_tools.cterm("input", "", "def")
        if command_name == "":
            continue
        try:
            if command_name != "help":
                completer.in_menu = False
            for module, commands in commands_list.items():
                if command_name in commands:
                    command = getattr(module, command_name)
                    break
            if command:
                command()
            else:
                crypto_tools.cterm('output', 'Error: incorrect command', 'err')
        except KeyError as err:
            crypto_tools.cterm("output", err, "err")
        completer.in_menu = True


if __name__ == "__main__":
    all_commands = []
    commands_list = {}
    for module in [algo, hack, crypto_commands]:
        commands_list[module] = dir(module)[9:]
        all_commands += commands_list[module]
    crypto_tools.render_static('header')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    readline.set_auto_history(False)
    main_loop()
