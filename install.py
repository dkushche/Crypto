#!/bin/python3

""" Install

TODO

Parameters
----------
TODO

Returns
-------
TODO

"""

import os
import sys
import platform
import subprocess

print("Start installation process")

subprocess.run(["python", "-m", "venv", "crypto_env" ], check=True)

if platform.system() == "Linux":
    subprocess.run(["crypto_env/bin/pip3", "install", "-r", "linux_requirements.txt"], check=True)

    _, folders, _ = next(os.walk("crypto_native"))
    for folder in folders:
        if folder != "__pycache__" and os.path.exists(f"crypto_native/{folder}/Makefile"):
            subprocess.run(["make", "-C", f"crypto_native/{folder}", "all", "clean"], check=True)

elif platform.system() == "Windows":
    subprocess.run([
        "crypto_env/Scripts/pip.exe", "install", "-r", "windows_requirements.txt"
    ], check=True)
else:
    print("Error: Unknown platform")
    sys.exit(1)

print("Installation finished")
