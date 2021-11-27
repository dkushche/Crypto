import ctypes
import os

import crypto_native.native_tools as native_tools


OPENSSL_API = None


def openssl_api_init():
    global OPENSSL_API
    OPENSSL_API = ctypes.cdll.LoadLibrary(f"{os.path.dirname(__file__)}/openssl_api.so")


def openssl_api_print_test(data, key, iv, mode):
    global OPENSSL_API

    data_buf = (ctypes.c_byte * len(data))
    data_buf = data_buf.from_buffer(data)
    data_array = native_tools.to_crypto_bytearray(data_buf)

    key_buf = (ctypes.c_byte * len(key))
    key_buf = key_buf.from_buffer(key)
    key_array = native_tools.to_crypto_bytearray(key_buf)

    iv_buf = (ctypes.c_byte * len(iv))
    iv_buf = iv_buf.from_buffer(iv)
    iv_array = native_tools.to_crypto_bytearray(iv_buf)

    mode_buf = (ctypes.c_char * len(mode))
    mode_buf = mode_buf.from_buffer(bytearray(mode, "utf-8"))

    OPENSSL_API.print_test.restype = None
    OPENSSL_API.print_test.argtypes = [
        ctypes.POINTER(native_tools.crypto_bytearray),
        ctypes.POINTER(native_tools.crypto_bytearray),
        ctypes.POINTER(native_tools.crypto_bytearray),
        ctypes.c_char_p
    ]

    OPENSSL_API.print_test(
        ctypes.pointer(data_array),
        ctypes.pointer(key_array),
        ctypes.pointer(iv_array),
        mode_buf
    )

    return True
