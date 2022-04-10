""" OpenSSL API

Layer between crypto modules and native OpenSSL
dynamic library

Parameters
----------
TODO

Returns
-------
TODO

"""

import ctypes
import os

from crypto_native import native_tools

class aes_128_args(ctypes.Structure):
    """
    Helper for passing arguments in function

    """
    _fields_ = [("data", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("key", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("iv", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("mode", ctypes.c_char_p),
                ("encrypt", ctypes.c_char_p)]

EVP_MAX_BLOCK_LENGTH = 32
openssl_api = None


def openssl_api_init():
    global openssl_api
    openssl_api = ctypes.cdll.LoadLibrary(f"{os.path.dirname(__file__)}/openssl_api.so")


def openssl_api_aes_128(data, key, iv, mode, encrypt):
    global openssl_api

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

    out_buf = native_tools.form_crypto_native_buffer(bytearray(len(data) + EVP_MAX_BLOCK_LENGTH))
    out_array = native_tools.to_crypto_bytearray(out_buf)

    openssl_api.aes_128.restype = ctypes.c_int
    openssl_api.aes_128.argtypes = [
        ctypes.POINTER(aes_128_args),
        ctypes.POINTER(native_tools.crypto_bytearray)
    ]
    result = openssl_api.aes_128(
        ctypes.pointer(args),
        ctypes.pointer(out_array)
    )

    if result == 0:
        return bytearray(out_buf)[:out_array.len]
    if result == 1:
        raise ValueError("Crypto_OpenSSL: library update cipher error")
    if result == 2:
        raise ValueError("Crypto_OpenSSL: library  final cipher error")
    raise ValueError("Crypto_OpenSSL: unexpected error")


def openssl_api_generate_rsa_keys(key_length, exponent,
                                  pem_key_filename, pub_key_filename):
    global openssl_api

    pem_key_filename_buf = native_tools.form_crypto_native_buffer(pem_key_filename)
    pub_key_filename_buf = native_tools.form_crypto_native_buffer(pub_key_filename)

    openssl_api.aes_128.restype = ctypes.c_int
    openssl_api.aes_128.argtypes = [
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_char_p,
        ctypes.c_char_p
    ]

    result = openssl_api.rsa_generate_keys(
        ctypes.c_ulong(key_length),
        ctypes.c_ulong(exponent),
        ctypes.cast(pem_key_filename_buf, ctypes.c_char_p),
        ctypes.cast(pub_key_filename_buf, ctypes.c_char_p)
    )

    if result == 1:
        raise ValueError("Crypto_OpenSSL: keys pair generation error")
    if result == 2:
        raise ValueError("Crypto_OpenSSL: private key file creation error")
    if result == 3:
        raise ValueError("Crypto_OpenSSL: public key file creation error")
    if result == 4:
        raise ValueError("Crypto_OpenSSL: private key writing error")
    if result == 5:
        raise ValueError("Crypto_OpenSSL: public key writing error")

    return "Keys generated in crypto_storage"

def openssl_api_rsa(data, encrypt, pem_key_filename, pub_key_filename):
    global openssl_api

    data_buf = native_tools.form_crypto_native_buffer(data)
    data_array = native_tools.to_crypto_bytearray(data_buf)

    out_buf = native_tools.form_crypto_native_buffer(bytearray(1024))
    out_array = native_tools.to_crypto_bytearray(out_buf)

    if encrypt == "encrypt":
        key_path =  native_tools.form_crypto_native_buffer(pub_key_filename)
        func = openssl_api.rsa_encrypt
    else:
        key_path =  native_tools.form_crypto_native_buffer(pem_key_filename)
        func = openssl_api.rsa_decrypt


    func.restype = ctypes.c_int
    func.argtypes = [
        ctypes.POINTER(native_tools.crypto_bytearray),
        ctypes.POINTER(native_tools.crypto_bytearray),
        ctypes.c_char_p
    ]

    result = func(
        ctypes.pointer(data_array),
        ctypes.pointer(out_array),
        ctypes.cast(key_path, ctypes.c_char_p)
    )

    if result == 1:
        raise ValueError("Crypto_OpenSSL: read key file error")
    if result == 2:
        raise ValueError("Crypto_OpenSSL: read key error")
    if result == 3:
        raise ValueError("Crypto_OpenSSL: math operation error")

    return bytearray(out_buf)[:out_array.len]


def openssl_api_random(size):
    global openssl_api

    out_buf = native_tools.form_crypto_native_buffer(bytearray(size))
    out_array = native_tools.to_crypto_bytearray(out_buf)

    openssl_api.random.restype = ctypes.c_int
    openssl_api.random.argtypes = [
        ctypes.POINTER(native_tools.crypto_bytearray)
    ]

    result = openssl_api.random(
        ctypes.pointer(out_array)
    )

    if result == 1:
        raise ValueError("Crypto_OpenSSL: random error")

    return bytearray(out_buf)
