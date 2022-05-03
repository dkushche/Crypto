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

import sys
import platform
import subprocess

print("Start installation process")

subprocess.run(["python", "-m", "venv", "crypto_env" ], check=True)

if platform.system() == "Linux":
    subprocess.run(["crypto_env/bin/pip3", "install", "-r", "linux_requirements.txt"], check=True)

    native_libs = [
        "native_tools",
        "openssl_api"
    ]
    for lib in native_libs:
        subprocess.run(["make", "-C", f"crypto_native/{lib}", "all", "clean"], check=True)

elif platform.system() == "Windows":
    subprocess.run([
        "crypto_env/Scripts/pip.exe", "install", "-r", "windows_requirements.txt"
    ], check=True)
else:
    print("Error: Unknown platform")
    sys.exit(1)

print("Installation finished")
