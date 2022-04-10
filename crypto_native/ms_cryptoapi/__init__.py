""" MS Crypto API

Layer between crypto modules and native MS Crypto API
dynamic library

Parameters
----------
TODO

Returns
-------
TODO

"""

import ctypes

from crypto_native import native_tools

CRYPT_EXPORTABLE = 0x1

HP_HASHVAL = 0x2

PLAINTEXTKEYBLOB = 0x8

PROV_RSA_AES = 0x18

CALG_AES_128 = 0x660E
CALG_AES_192 = 0x660F
CALG_AES_256 = 0x6610
CALG_SHA_256 = 0x800C

BCRYPT_BLOCK_PADDING = 0x1

def check_result(provider, result, desc):
    if provider == "standard":
        if not result:
            raise ValueError(f"Crypto_MS_CRYPTOAPI: {desc}")
    else:
        if result < 0:
            raise ValueError(f"Crypto_MS_CRYPTOAPI: {desc}")


def ms_cryptoapi_standard_aes(data, key, encrypt):
    ms_cryptoapi = ctypes.windll.advapi32

    ctx_ptr = ctypes.c_void_p()
    hash_ptr = ctypes.c_void_p()

    result = ms_cryptoapi.CryptAcquireContextA(
        ctypes.byref(ctx_ptr), 0, 0, PROV_RSA_AES, 0
    )
    check_result("standard", result, "context creation error")

    result = ms_cryptoapi.CryptCreateHash(
        ctx_ptr, CALG_SHA_256, 0, 0, ctypes.byref(hash_ptr)
    )
    check_result("standard", result, "hash initialization error")

    key = ctypes.create_string_buffer(bytes(key), len(key))
    result = ms_cryptoapi.CryptHashData(
        hash_ptr, key, ctypes.sizeof(key), 0
    )
    check_result("standard", result, "hash data initialization error")

    hashed_key_len = ctypes.c_int(32)
    hashed_key = ctypes.create_string_buffer(b'', hashed_key_len.value)
    result = ms_cryptoapi.CryptGetHashParam(
        hash_ptr, HP_HASHVAL, hashed_key, ctypes.byref(hashed_key_len), 0
    )
    check_result("standard", result, "set hash parameters error")

    algorithms = {128: CALG_AES_128, 192: CALG_AES_192, 256: CALG_AES_256}
    hkey = ctypes.c_void_p()
    result = ms_cryptoapi.CryptDeriveKey(
        ctx_ptr, algorithms[len(key) * 8],
        hash_ptr, CRYPT_EXPORTABLE, ctypes.byref(hkey)
    )
    check_result("standard", result, "generating cryptographic session keys error")

    key_len = ctypes.c_int(0)
    result = ms_cryptoapi.CryptExportKey(
        hkey, 0, PLAINTEXTKEYBLOB, 0, 0, ctypes.byref(key_len)
    )
    check_result("standard", result, "check key length error")

    key_data = ctypes.create_string_buffer(b'', key_len.value)
    result = ms_cryptoapi.CryptExportKey(
        hkey, 0, PLAINTEXTKEYBLOB, 0, key_data, ctypes.byref(key_len)
    )
    check_result("standard", result, "export key error")

    if encrypt == "encrypt":
        data_len = ctypes.c_int(len(data))
        result = ms_cryptoapi.CryptEncrypt(
            hkey, 0, 1, 0, 0, ctypes.byref(data_len), len(data)
        )
        check_result("standard", result, "pre encryption error")

        out_data = ctypes.create_string_buffer(bytes(data), data_len.value)
        result = ms_cryptoapi.CryptEncrypt(
            hkey, 0, 1, 0, out_data,
            ctypes.byref(ctypes.c_int(len(data))), data_len.value
        )
        check_result("standard", result, "encryption error")

        out_data = out_data.raw
    else:
        data_len = ctypes.c_int(len(data))
        out_data = ctypes.create_string_buffer(bytes(data), len(data))

        result = ms_cryptoapi.CryptDecrypt(
            hkey, 0, 1, 0, out_data, ctypes.byref(data_len)
        )
        check_result("standard", result, "decryption error")

        out_data = out_data.raw[:data_len.value]

    result = ms_cryptoapi.CryptDestroyKey(hkey)
    check_result("standard", result, "key destruction error")

    result = ms_cryptoapi.CryptDestroyHash(hash_ptr)
    check_result("standard", result, "hesh destruction error")

    result = ms_cryptoapi.CryptReleaseContext(ctx_ptr, 0)
    check_result("standard", result, "context destruction error")

    return {
        "hashed_key": hashed_key.raw.hex(),
        "session_key": key_data.raw[12:].hex(),
        "result": out_data
    }


def ms_cryptoapi_nextgen_gen_hash(ms_cryptoapi, key):
    hash_ctx = ctypes.c_void_p()
    result = ms_cryptoapi.BCryptOpenAlgorithmProvider(
        ctypes.byref(hash_ctx), ctypes.c_wchar_p('SHA256'), 0, 0
    )
    check_result("nextgen", result, "sha-256 algorithm provider error")

    h_hash = ctypes.c_void_p()
    cb_hash_obj = ctypes.c_uint(326)
    pb_hash_obj = ctypes.create_string_buffer(b'', cb_hash_obj.value)
    result = ms_cryptoapi.BCryptCreateHash(
        hash_ctx, ctypes.byref(h_hash), pb_hash_obj, cb_hash_obj, 0, 0, 0x20
    )
    check_result("nextgen", result, "hash algo creation error")

    key_buffer = ctypes.create_string_buffer(bytes(key), len(key))
    result = ms_cryptoapi.BCryptHashData(
        h_hash, key_buffer, ctypes.sizeof(key_buffer), 0
    )
    check_result("nextgen", result, "hashing error")

    cb_hash = ctypes.c_uint(32)
    pb_hash = ctypes.create_string_buffer(b'', 32)
    result = ms_cryptoapi.BCryptFinishHash(
        h_hash, pb_hash, cb_hash, 0
    )
    check_result("nextgen", result, "finish hashing error")

    result = ms_cryptoapi.BCryptDestroyHash(h_hash)
    check_result("nextgen", result, "hash destruction error")

    return hash_ctx, pb_hash


def ms_cryptoapi_nextgen_aes(data, key, mode, encrypt):
    ms_cryptoapi = ctypes.windll.bcrypt

    hash_ctx, pb_hash = ms_cryptoapi_nextgen_gen_hash(
        ms_cryptoapi, key
    )

    aes_ctx = ctypes.c_void_p()
    result = ms_cryptoapi.BCryptOpenAlgorithmProvider(
        ctypes.byref(aes_ctx), ctypes.c_wchar_p('AES'), 0, 0
    )
    check_result("nextgen", result, "aes algorithm provider error")

    chaining_modes = {
        "CBC": ctypes.c_wchar_p('ChainingModeCBC'),
        'ECB': ctypes.c_wchar_p('ChainingModeECB'),
        'CFB': ctypes.c_wchar_p('ChainingModeCFB')
    }
    result = ms_cryptoapi.BCryptSetProperty(
        aes_ctx, ctypes.c_wchar_p('ChainingMode'),
        chaining_modes[mode], ctypes.sizeof(chaining_modes[mode]), 0
    )
    check_result("nextgen", result, "property setting error")

    pb_key = ctypes.create_string_buffer(pb_hash.raw[:len(key)], len(key))

    h_key = ctypes.c_void_p()
    pb_key_obj = ctypes.create_string_buffer(b'', 654)
    result = ms_cryptoapi.BCryptGenerateSymmetricKey(
        aes_ctx, ctypes.byref(h_key), pb_key_obj,
        ctypes.c_uint(654), pb_key, ctypes.sizeof(pb_key), 0
    )
    check_result("nextgen", result, "genereting symmetric key error")

    pb_iv = ctypes.create_string_buffer( b'\x00' * 16, 16) if mode != 'ECB' else 0
    cb_iv = ctypes.c_uint(16) if mode != 'ECB' else 0

    cb_out = ctypes.c_uint(0)
    data_buf = ctypes.create_string_buffer(bytes(data), len(data))

    if encrypt == "encrypt":
        result = ms_cryptoapi.BCryptEncrypt(
            h_key, data_buf, ctypes.sizeof(data_buf),
            0, pb_iv, cb_iv, 0, 0,  ctypes.byref(cb_out), BCRYPT_BLOCK_PADDING
        )
        check_result("nextgen", result, "cryptography initialization error")

        pb_out = ctypes.create_string_buffer(b'', cb_out.value)
        cb_data = ctypes.c_uint(0)
        result = ms_cryptoapi.BCryptEncrypt(
            h_key, data_buf, ctypes.sizeof(data_buf),
            0, pb_iv, cb_iv, pb_out, cb_out, ctypes.byref(cb_data), BCRYPT_BLOCK_PADDING
        )
        check_result("nextgen", result, "encryption error")

        pb_out = pb_out.raw
    else:
        result = ms_cryptoapi.BCryptDecrypt(
            h_key, data_buf, ctypes.sizeof(data_buf),
            0, pb_iv, cb_iv, 0, 0, ctypes.byref(cb_out), BCRYPT_BLOCK_PADDING
        )
        check_result("nextgen", result, "cryptography initialization error")

        pb_out = ctypes.create_string_buffer(b'', cb_out.value)
        result = ms_cryptoapi.BCryptDecrypt(
            h_key, data_buf, ctypes.sizeof(data_buf),
            0, pb_iv, cb_iv, pb_out, cb_out, ctypes.byref(cb_out), BCRYPT_BLOCK_PADDING
        )
        check_result("nextgen", result, "decryption error")

        pb_out = pb_out.raw.rstrip(b'\x00')

    result = ms_cryptoapi.BCryptDestroyKey(h_key)
    check_result("nextgen", result, "key desturction error")
    result = ms_cryptoapi.BCryptCloseAlgorithmProvider(hash_ctx, 0)
    check_result("nextgen", result, "hash context destruction error")
    result = ms_cryptoapi.BCryptCloseAlgorithmProvider(aes_ctx, 0)
    check_result("nextgen", result, "aes context destruction error")

    return {
        "hashed_key": pb_hash.raw.hex(),
        "session_key": pb_key.raw.hex(),
        "result": pb_out
    }
