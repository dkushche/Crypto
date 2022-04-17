#!/bin/python3

""" Crypto

TODO

Parameters
----------
TODO

Returns
-------
TODO

"""

import sys
import platform
import subprocess

if platform.system() == "Linux":
    subprocess.run(["crypto_env/bin/python", "core.py", *sys.argv[1:]], check=False)
elif platform.system() == "Windows":
    subprocess.run(["crypto_env/Scripts/python.exe", "core.py", *sys.argv[1:]], check=False)
else:
    print("Error: Unknown platform")
    sys.exit(1)
