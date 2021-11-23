import ctypes
import os

OPENSSL_API = None

def openssl_api_init():
    global OPENSSL_API

    OPENSSL_API = ctypes.cdll.LoadLibrary(f"{os.path.dirname(__file__)}/openssl_api.so")

def openssl_api_add(a, b):
    return OPENSSL_API.add(a, b)
