import ctypes
import os

import crypto_native.native_tools as native_tools

CRYPT_EXPORTABLE = 0x1

HP_HASHVAL = 0x2

PLAINTEXTKEYBLOB = 0x8

PROV_RSA_AES = 0x18

CALG_AES_128 = 0x660E
CALG_AES_192 = 0x660F
CALG_AES_256 = 0x6610
CALG_SHA_256 = 0x800C


def check_result(result, desc):
    if not result:
        raise ValueError(f"Crypto_MS_CRYPTOAPI: {desc}")


def ms_cryptoapi_standard_aes(data, key, encrypt):
    MS_CRYPTOAPI = ctypes.windll.advapi32

    ctx_ptr = ctypes.c_void_p()
    hash_ptr = ctypes.c_void_p()

    result = MS_CRYPTOAPI.CryptAcquireContextA(
        ctypes.byref(ctx_ptr), 0, 0, PROV_RSA_AES, 0
    )
    check_result(result, "context creation error")

    result = MS_CRYPTOAPI.CryptCreateHash(
        ctx_ptr, CALG_SHA_256, 0, 0, ctypes.byref(hash_ptr)
    )
    check_result(result, "hash initialization error")

    key = ctypes.create_string_buffer(bytes(key), len(key))
    result = MS_CRYPTOAPI.CryptHashData(
        hash_ptr, key, ctypes.sizeof(key), 0
    )
    check_result(result, "hash data initialization error")

    hashed_key_len = ctypes.c_int(32)
    hashed_key = ctypes.create_string_buffer(b'', hashed_key_len.value)
    result = MS_CRYPTOAPI.CryptGetHashParam(
        hash_ptr, HP_HASHVAL, hashed_key, ctypes.byref(hashed_key_len), 0
    )
    check_result(result, "set hash parameters error")

    algorithms = {128: CALG_AES_128, 192: CALG_AES_192, 256: CALG_AES_256}
    hkey = ctypes.c_void_p()
    result = MS_CRYPTOAPI.CryptDeriveKey(
        ctx_ptr, algorithms[len(key) * 8],
        hash_ptr, CRYPT_EXPORTABLE, ctypes.byref(hkey)
    )
    check_result(result, "generating cryptographic session keys error")

    key_len = ctypes.c_int(0)
    result = MS_CRYPTOAPI.CryptExportKey(
        hkey, 0, PLAINTEXTKEYBLOB, 0, 0, ctypes.byref(key_len)
    )
    check_result(result, "check key length error")

    key_data = ctypes.create_string_buffer(b'', key_len.value)
    result = MS_CRYPTOAPI.CryptExportKey(
        hkey, 0, PLAINTEXTKEYBLOB, 0, key_data, ctypes.byref(key_len)
    )
    check_result(result, "export key error")

    if encrypt == "encrypt":
        data_len = ctypes.c_int(len(data))
        result = MS_CRYPTOAPI.CryptEncrypt(
            hkey, 0, 1, 0, 0, ctypes.byref(data_len), len(data)
        )
        check_result(result, "pre encryption error")

        out_data = ctypes.create_string_buffer(bytes(data), data_len.value)
        result = MS_CRYPTOAPI.CryptEncrypt(
            hkey, 0, 1, 0, out_data,
            ctypes.byref(ctypes.c_int(len(data))), data_len.value
        )
        check_result(result, "encryption error")

        out_data = out_data.raw
    else:
        data_len = ctypes.c_int(len(data))
        out_data = ctypes.create_string_buffer(bytes(data), len(data))

        result = MS_CRYPTOAPI.CryptDecrypt(
            hkey, 0, 1, 0, out_data, ctypes.byref(data_len)
        )
        check_result(result, "decryption error")

        out_data = out_data.raw[:data_len.value]

    return {
        "hashed_key": hashed_key.raw.hex(),
        "session_key": key_data.raw[12:].hex(),
        "result": out_data
    }


def ms_cryptoapi_nextgen_aes(data, key, mode, encrypt):
    MS_CRYPTOAPI = ctypes.windll.bcrypt
