from json import load as get_json
from .caesar import *
from .caesar_hacking import *
from .playfair import *
from .xor import *


algo_run = None
try:
    with open("algo/algo_run.json") as algo:
        algo_run = get_json(algo)
except FileNotFoundError:
    print("\033[31mError: no algo_run.json in algo package\033[0m")
    exit()
