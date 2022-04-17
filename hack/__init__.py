""" Cryptoanalysis modules

Module imports all public entry points that will be available from CLI

"""

from .fips140_random_test import fips140_random_test
from .brute_force import brute_force
from .freq_analys import freq_analys
from .rsa_hijack import rsa_hijack


def __doc__():
    return "Cryptoanalysis module:"
