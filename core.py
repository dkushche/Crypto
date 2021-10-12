import crypto_commands
import crypto_tools
import readline
import algo
import hack
import sys


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
    try:
        all_commands = []
        commands_list = {}
        for module in [algo, hack, crypto_commands]:
            commands_list[module] = dir(module)[9:]
            all_commands += commands_list[module]
        if len(sys.argv) == 2:
            crypto_tools.iface_init(sys.argv[1])
        else:
            crypto_tools.iface_init("iface_storage/default_profile/")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)
        readline.set_auto_history(False)
        main_loop()
    except KeyboardInterrupt:
        crypto_tools.cterm('output', 'force_exit', 'inf')
