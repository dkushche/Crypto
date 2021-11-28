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

    data_buf = native_tools.form_crypto_native_buffer(data)
    data_array = native_tools.to_crypto_bytearray(data_buf)

    key_buf = native_tools.form_crypto_native_buffer(key)
    key_array = native_tools.to_crypto_bytearray(key_buf)

    iv_buf = native_tools.form_crypto_native_buffer(iv)
    iv_array = native_tools.to_crypto_bytearray(iv_buf)

    mode_buf = native_tools.form_crypto_native_buffer(mode)
    enc_buf = native_tools.form_crypto_native_buffer(encrypt)

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


def openssl_api_rsa_generate_keys(key_length, exponent,
                                  pem_key_filename, pub_key_filename):
    global OPENSSL_API

    pem_key_filename_buf = native_tools.form_crypto_native_buffer(pem_key_filename)
    pub_key_filename_buf = native_tools.form_crypto_native_buffer(pub_key_filename)

    OPENSSL_API.aes_128.restype = ctypes.c_int
    OPENSSL_API.aes_128.argtypes = [
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_char_p,
        ctypes.c_char_p
    ]

    result = OPENSSL_API.rsa_generate_keys(
        ctypes.c_ulong(key_length),
        ctypes.c_ulong(exponent),
        ctypes.cast(pem_key_filename_buf, ctypes.c_char_p),
        ctypes.cast(pub_key_filename_buf, ctypes.c_char_p)
    )

    if result == 0:
        return "Keys generated in crypto_storage"
