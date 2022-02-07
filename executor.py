#!/bin/python3

import sys
import platform
import subprocess

if platform.system() == "Linux":
    sys.argv[0] = f"linux_platform/{sys.argv[0][2:]}"
    subprocess.call(sys.argv)
elif platform.system() == "Windows":
    sys.argv[0] = f"windows_platform\{sys.argv[0]}.bat"
    subprocess.call(sys.argv)
else:
    print("Error: Unknown platform")
