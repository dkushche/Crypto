#!/bin/python3

""" Executor

Helps in running cross platform tools
Actually looks like shit and terminal realizations
should be rewritten in python

"""

import sys
import platform
import subprocess

if platform.system() == "Linux":
    sys.argv[0] = fr"linux_platform/{sys.argv[0][2:]}"
    subprocess.call(sys.argv)
elif platform.system() == "Windows":
    sys.argv[0] = fr"windows_platform\{sys.argv[0]}.bat"
    subprocess.call(sys.argv)
else:
    print("Error: Unknown platform")
