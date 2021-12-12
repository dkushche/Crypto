from .openssl_generate_rsa_keys import openssl_generate_rsa_keys
from .openssl_aes_128 import openssl_aes_128
from .lfsr_generator import lfsr_generator
from .openssl_random import openssl_random
from .diffie_hellman import diffie_hellman
from .openssl_rsa import openssl_rsa
from .ansi_x9_17 import ansi_x9_17
from .triple_des import triple_des
from .dummy_rsa import dummy_rsa
from .elliptic import elliptic
from .vigenere import vigenere
from .elgamal import elgamal
from .random import random
from .caesar import caesar
from .block import block
from .magma import magma
from .hill import hill
from .hash import hash
from .lfsr import lfsr
from .des import des
from .xor import xor
from .rc4 import rc4
from .rsa import rsa
from .dsa import dsa

import platform

if platform.system() == 'Windows':
    from .cryptoapi_aes import cryptoapi_aes

def __doc__():
    return f"Cryptography module"
