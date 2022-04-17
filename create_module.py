#!/bin/python3

""" Create crypto module

TODO

Parameters
----------
TODO

Returns
-------
TODO

"""

import sys

if len(sys.argv) == 3:
    if sys.argv[1] in ("algo", "hack"):
        with open(f"{sys.argv[1]}/{sys.argv[2]}.py", 'w+') as crypto_module:
            crypto_module.write(f"""\"\"\" {sys.argv[2]}

TODO

Parameters
----------
TODO

Returns
-------
TODO

\"\"\"

import crypto_tools


def {sys.argv[2]}_little_doc():
    return \"{sys.argv[2]}_little_doc\"


def {sys.argv[2]}_full_doc():
    return \"\"\"
    {sys.argv[2]}_full_doc
    \"\"\"


def {sys.argv[2]}_processing(data, key):
    return data


@crypto_tools.file_manipulation()
def {sys.argv[2]}(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    return {sys.argv[2]}_processing(data, key)


{sys.argv[2]}.little_doc = {sys.argv[2]}_little_doc
{sys.argv[2]}.full_doc = {sys.argv[2]}_full_doc
""")

        res = None
        with open(f"{sys.argv[1]}/__init__.py", "r") as init_file:
            init = init_file.read().split("\n")
            module_line = f"from .{sys.argv[2]} import {sys.argv[2]}"
            found = False
            for i in range(len(init)):
                if "from ." not in init[i] and found:
                    init.insert(i, module_line)
                    break
                if "from ." in init[i]:
                    found = True
                    if len(module_line) >= len(init[i]):
                        init.insert(i, module_line)
                        break
            res = '\n'.join(init)

        with open(f"{sys.argv[1]}/__init__.py", "w") as init_file:
            init_file.write(res)

        sys.exit(1)

print(f"Usage: {sys.argv[0]} algo|hack module_name")
