""" OpenSSL AES 128

AES using OpenSSL native shared dynamic library with 128 bit key

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools
import crypto_native


def openssl_aes_128_little_doc():
    return "short example of encryption and decryption using openssl"


def openssl_aes_128_full_doc():
    return """
    openssl_aes_128_full_doc
    """


def openssl_aes_128_pre_processing(key, init_vec):
    if len(key) > 16:
        raise ValueError("Too big key. Max len required: 16")
    crypto_tools.supl_to_mult(key, 16)

    if len(init_vec) > 16:
        raise ValueError("Too big initialization vector. Max len required: 16")
    crypto_tools.supl_to_mult(init_vec, 16)


def openssl_aes_128_processing(data, key, init_vec, mode, encrypt):
    openssl_aes_128_pre_processing(key, init_vec)

    crypto_native.openssl_api_init()

    result = crypto_native.openssl_api_aes_128(data, key, init_vec, mode, encrypt)

    return result


@crypto_tools.file_manipulation()
def openssl_aes_128(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    init_vec = crypto_tools.cterm('input', 'Enter initialization vector(str): ', 'ans')
    if init_vec.__class__ == str:
        init_vec = bytearray(init_vec.encode())

    mode = crypto_tools.cterm(
        'input',
        'Enter mode(CBC(Cipher Block Chaining)|CFB(Cipher Feedback)): ',
        'ans'
    )
    if mode not in ["CBC", "CFB"]:
        raise ValueError(f"Incorrect mode: {mode}")

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    res_data = openssl_aes_128_processing(data, key, init_vec, mode, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


openssl_aes_128.little_doc = openssl_aes_128_little_doc
openssl_aes_128.full_doc = openssl_aes_128_full_doc
