#!/bin/bash

test -e crypto_env
if [[ "$?" -eq "1" ]]; then
    echo "Start installation process"
    python3 -m venv crypto_env
    source crypto_env/bin/activate
    pip install -r requirements.txt
    echo "Installed"
else
    echo "Already installed"
fi
