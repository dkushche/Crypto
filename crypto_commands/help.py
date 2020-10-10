import algo
import hack
import crypto_tools


def help_process_input(commands_list):
    while True:
        full_doc = None
        quest = 'Write command name for more info or "back": '
        command = crypto_tools.cterm('input', quest, 'ans')
        if command == "back":
            break
        if command in ["help", "exit", "force_exit"]:
            crypto_tools.cterm('output',
                               "O'rly, It's too easy, I hope it's a joke",
                               'inf')
            continue
        try:
            for module, commands in commands_list.items():
                if command in commands:
                    full_doc = getattr(module, f"{command}").full_doc()
        except AttributeError:
            crypto_tools.cterm('output',
                               'No detailed description for this command',
                               'err')
            continue

        if full_doc:
            crypto_tools.cterm("output", full_doc, "inf")
        else:
            crypto_tools.cterm('output', 'No such command', 'err')


def general_help(commands_list):
    crypto_tools.cterm("output", "Crypto helper:", "inf")
    for module, commands in commands_list.items():
        crypto_tools.cterm('output', "*-" * 30 + "\n", "inf")
        crypto_tools.cterm('output', f"{module.__doc__()}:", "inf")
        for command in commands:
            try:
                descr = "{:15} ->\t\t{}".format(
                    command,
                    getattr(module, f"{command}").little_doc()
                )
                crypto_tools.cterm("output", descr, "inf")
            except AttributeError:
                no_desc = "{:15} ->\t\tNo description"
                crypto_tools.cterm("output",
                                   no_desc.format(command), "inf")
        crypto_tools.cterm("output", "", "inf")
    crypto_tools.cterm('output', "*-" * 30 + "\n", "inf")
    crypto_tools.cterm("output",
                       "{:15} ->\t\tshow this message".format("help"), "inf")
    crypto_tools.cterm("output",
                       "{:15} ->\t\tturn off crypto".format("exit"), "inf")
    crypto_tools.cterm("output",
                       "{:15} ->\t\tturn off crypto with keyboard interrupt\
                        \n".format("force_exit"), "inf")
    crypto_tools.cterm('output', "*-" * 30 + "\n", "inf")


def help():
    commands_modules = [algo, hack]
    commands_list = {}
    for module in commands_modules:
        commands_list[module] = dir(module)[9:]
    general_help(commands_list)
    help_process_input(commands_list)
