import ctypes
import os

import crypto_native.native_tools as native_tools

class aes_128_args(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("key", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("iv", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("mode", ctypes.c_char_p),
                ("encrypt", ctypes.c_char_p)]


OPENSSL_API = None


def openssl_api_init():
    global OPENSSL_API
    OPENSSL_API = ctypes.cdll.LoadLibrary(f"{os.path.dirname(__file__)}/openssl_api.so")


def openssl_api_aes_128(data, key, iv, mode, encrypt):
    global OPENSSL_API

    data_buf = (ctypes.c_byte * len(data))
    data_buf = data_buf.from_buffer(bytearray(data))
    data_array = native_tools.to_crypto_bytearray(data_buf)

    key_buf = (ctypes.c_byte * len(key))
    key_buf = key_buf.from_buffer(bytearray(key))
    key_array = native_tools.to_crypto_bytearray(key_buf)

    iv_buf = (ctypes.c_byte * len(iv))
    iv_buf = iv_buf.from_buffer(bytearray(iv))
    iv_array = native_tools.to_crypto_bytearray(iv_buf)

    mode_buf = (ctypes.c_char * len(mode))
    mode_buf = mode_buf.from_buffer(bytearray(mode, "utf-8"))

    enc_buf = (ctypes.c_char * len(encrypt))
    enc_buf = enc_buf.from_buffer(bytearray(encrypt, "utf-8"))

    args = aes_128_args(
        data=ctypes.pointer(data_array),
        key=ctypes.pointer(key_array),
        iv=ctypes.pointer(iv_array),
        mode=ctypes.cast(mode_buf, ctypes.c_char_p),
        encrypt=ctypes.cast(enc_buf, ctypes.c_char_p)
    )

    EVP_MAX_BLOCK_LENGTH = 32
    out_len = len(data) + EVP_MAX_BLOCK_LENGTH
    out_buf = (ctypes.c_byte * out_len)
    out_buf = out_buf.from_buffer(bytearray(out_len))
    out_array = native_tools.to_crypto_bytearray(out_buf)

    OPENSSL_API.aes_128.restype = ctypes.c_int
    OPENSSL_API.aes_128.argtypes = [
        ctypes.POINTER(aes_128_args),
        ctypes.POINTER(native_tools.crypto_bytearray)
    ]
    result = OPENSSL_API.aes_128(
        ctypes.pointer(args),
        ctypes.pointer(out_array)
    )

    if result == 0:
        return bytearray(out_buf)[:out_array.len]
    elif result == 1:
        raise ValueError("Crypto_OpenSSL library update cipher error")
    elif result == 2:
        raise ValueError("Crypto_OpenSSL library  final cipher error")
    else:
        raise ValueError("Crypto_OpenSSL: unexpected error")
