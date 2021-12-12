import ctypes
import os

import crypto_native.native_tools as native_tools

MS_CRYPTOAPI = None


def openssl_api_init():
    global MS_CRYPTOAPI
