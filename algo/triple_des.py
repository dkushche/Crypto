""" Triple DES

In cryptography, Triple DES (3DES or TDES), officially the
Triple Data Encryption Algorithm (TDEA or Triple DEA), is
a symmetric-key block cipher, which applies the DES cipher
algorithm three times to each data block. The Data Encryption Standard's (DES)
56-bit key is no longer considered adequate in the face of modern cryptanalytic
techniques and supercomputing power. A CVE released in 2016, CVE-2016-2183
disclosed a major security vulnerability in DES and 3DES encryption algorithms.
This CVE, combined with the inadequate key size of DES and 3DES, NIST has
deprecated DES and 3DES for new applications in 2017, and for all applications by 2023.
It has been replaced with the more secure, more robust AES.

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools
from .des import des_processing


def triple_des_little_doc():
    return "triple_des_little_doc"


def triple_des_full_doc():
    return """
    triple_des_full_doc
    """


def triple_des_pre_processing(key):
    if len(key) > 7 * 3:
        raise ValueError(f"Too big key. Max len required: {7 * 3}")
    crypto_tools.supl_to_mult(key, 7 * 3)


def triple_des_processing(data, key, encrypt):
    triple_des_pre_processing(key)

    sub_keys = [key[i:i + 7] for i in range(0, len(key), 7)]

    cur_encrypt = encrypt

    for i in range(3):
        sub_key = sub_keys[i] if encrypt == "encrypt" else sub_keys[2 - i]

        data = des_processing(data, sub_key, cur_encrypt)

        cur_encrypt = "decrypt" if cur_encrypt == "encrypt" else "encrypt"

    return data


@crypto_tools.file_manipulation()
def triple_des(data):
    if data.__class__ == str:
        data = bytearray(data.encode())

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    res_data = triple_des_processing(data, key, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


triple_des.little_doc = triple_des_little_doc
triple_des.full_doc = triple_des_full_doc
