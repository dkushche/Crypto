import ctypes
import os

import crypto_native.native_tools as native_tools

class aes_128_args(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("key", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("iv", ctypes.POINTER(native_tools.crypto_bytearray)),
                ("mode", ctypes.c_char_p),
                ("encrypt", ctypes.c_char_p)]

EVP_MAX_BLOCK_LENGTH = 32
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

    out_buf = native_tools.form_crypto_native_buffer(bytearray(len(data) + EVP_MAX_BLOCK_LENGTH))
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
        raise ValueError("Crypto_OpenSSL: library update cipher error")
    elif result == 2:
        raise ValueError("Crypto_OpenSSL: library  final cipher error")
    else:
        raise ValueError("Crypto_OpenSSL: unexpected error")


def openssl_api_generate_rsa_keys(key_length, exponent,
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
    elif result == 1:
        raise ValueError("Crypto_OpenSSL: keys pair generation error")
    elif result == 2:
        raise ValueError("Crypto_OpenSSL: private key file creation error")
    elif result == 3:
        raise ValueError("Crypto_OpenSSL: public key file creation error")
    elif result == 4:
        raise ValueError("Crypto_OpenSSL: private key writing error")
    elif result == 5:
        raise ValueError("Crypto_OpenSSL: public key writing error")


def openssl_api_rsa(data, encrypt, pem_key_filename, pub_key_filename):
    global OPENSSL_API

    data_buf = native_tools.form_crypto_native_buffer(data)
    data_array = native_tools.to_crypto_bytearray(data_buf)

    out_buf = native_tools.form_crypto_native_buffer(bytearray(1024))
    out_array = native_tools.to_crypto_bytearray(out_buf)

    if encrypt == "encrypt":
        pub_key_filename_buf = native_tools.form_crypto_native_buffer(pub_key_filename)

        OPENSSL_API.rsa_encrypt.restype = ctypes.c_int
        OPENSSL_API.rsa_encrypt.argtypes = [
            ctypes.POINTER(native_tools.crypto_bytearray),
            ctypes.POINTER(native_tools.crypto_bytearray),
            ctypes.c_char_p
        ]

        result = OPENSSL_API.rsa_encrypt(
            ctypes.pointer(data_array),
            ctypes.pointer(out_array),
            ctypes.cast(pub_key_filename_buf, ctypes.c_char_p)
        )
    else:
        pem_key_filename_buf = native_tools.form_crypto_native_buffer(pem_key_filename)

        OPENSSL_API.rsa_decrypt.restype = ctypes.c_int
        OPENSSL_API.rsa_decrypt.argtypes = [
            ctypes.POINTER(native_tools.crypto_bytearray),
            ctypes.POINTER(native_tools.crypto_bytearray),
            ctypes.c_char_p
        ]

        result = OPENSSL_API.rsa_decrypt(
            ctypes.pointer(data_array),
            ctypes.pointer(out_array),
            ctypes.cast(pem_key_filename_buf, ctypes.c_char_p)
        )

    if result == 0:
        return bytearray(out_buf)[:out_array.len]
    elif result == 1:
        raise ValueError("Crypto_OpenSSL: read key error")
    elif result == 2:
        raise ValueError("Crypto_OpenSSL: math operation error")
