""" XOR

The XOR operator is extremely common as a component in more complex ciphers.
By itself, using a constant repeating key, a simple XOR cipher can trivially
be broken using frequency analysis. If the content of any message can be guessed
or otherwise known then the key can be revealed. Its primary merit is that it is
simple to implement, and that the XOR operation is computationally inexpensive.
A simple repeating XOR (i.e. using the same key for xor operation on the whole data)
cipher is therefore sometimes used for hiding information in cases where no particular
security is required. The XOR cipher is often used in computer malware to make reverse
engineering more difficult.

Parameters
----------
TODO

Returns
-------
TODO

"""

from itertools import cycle
import crypto_tools


def xor_little_doc():
    return "encrypt/decrypt using xor algo"


def xor_full_doc():
    return """
    Xor algorithm.
    Xor your data with repeating key
    """


def xor_processing(data, key, encrypt):
    key_bytes = cycle(key)
    if encrypt == "encrypt" and data.__class__ == str:
        data_in_bytes = bytearray(data, "utf-8")
    else:
        data_in_bytes = data
    result_bytes = bytearray(a ^ b for a, b in zip(data_in_bytes, key_bytes))
    if encrypt == "encrypt":
        result_str = result_bytes
    else:
        result_str = result_bytes.decode("utf-8")
    return result_str


@crypto_tools.file_manipulation()
def xor(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect action")
    if len(key) == 0:
        raise ValueError("Empty key")
    if key.__class__ == str:
        key = bytearray(key, "utf-8")
    return xor_processing(data, key, encrypt)


xor.little_doc = xor_little_doc
xor.full_doc = xor_full_doc
