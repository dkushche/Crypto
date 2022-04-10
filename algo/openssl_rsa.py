""" RSA

RSA cypher using OpenSSL native shared dynamic library

Parameters
----------
TODO

Returns
-------
TODO

"""

import os

import crypto_tools
import crypto_native


def openssl_rsa_little_doc():
    return "openssl_rsa_little_doc"


def openssl_rsa_full_doc():
    return """
    openssl_rsa_full_doc
    """


def openssl_rsa_processing(data, encrypt, pem_key_filename, pub_key_filename):
    crypto_native.openssl_api_init()

    result = crypto_native.openssl_api_rsa(
        data, encrypt, pem_key_filename, pub_key_filename
    )

    return result


@crypto_tools.file_manipulation()
def openssl_rsa(data):
    if not os.path.exists("storage/"):
        raise ValueError("Can't find storage directory with keys")

    pem_key_filename = crypto_tools.cterm('input', 'Enter private key filename(str): ', 'ans')
    pem_key_filename = "storage/" + pem_key_filename

    pub_key_filename = crypto_tools.cterm('input', 'Enter public key filename(str): ', 'ans')
    pub_key_filename = "storage/" + pub_key_filename

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    res_data = openssl_rsa_processing(data, encrypt, pem_key_filename, pub_key_filename)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


openssl_rsa.little_doc = openssl_rsa_little_doc
openssl_rsa.full_doc = openssl_rsa_full_doc
