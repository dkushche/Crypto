""" RC4

RC4 (Rivest Cipher 4 also known as ARC4 or ARCFOUR meaning Alleged RC4)
is a stream cipher. While it is remarkable for its simplicity and speed
in software, multiple vulnerabilities have been discovered in RC4, rendering it insecure.
It is especially vulnerable when the beginning of the output keystream is not discarded,
or when nonrandom or related keys are used. Particularly problematic uses of RC4 have
led to very insecure protocols such as WEP.

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools


def rc4_little_doc():
    return "find arguments/create random sequences"


def rc4_full_doc():
    return """
    Input example for generate:
        {"size": 10, "amount": 2}
    Input example for calc:
    [
        {"a": 21, "c": 1, "f": 0, "m": 100},
        {"a": 21, "c": 3, "f": 0, "m": 100},
        {"a": 21, "c": 7, "f": 0, "m": 100},
        {"a": 21, "c": 9, "f": 0, "m": 100},
        {"a": 21, "c": 11, "f": 0, "m": 100},
        {"a": 21, "c": 13, "f": 0, "m": 100},
        {"a": 21, "c": 17, "f": 0, "m": 100}
    ]
    """


def rc4_prga(scheduled_key):
    rc4_prga.x = (rc4_prga.x + 1) % 256
    rc4_prga.y = (rc4_prga.y + scheduled_key[rc4_prga.x]) % 256

    scheduled_buffer = scheduled_key[rc4_prga.x]
    scheduled_key[rc4_prga.x] = scheduled_key[rc4_prga.y]
    scheduled_key[rc4_prga.y] = scheduled_buffer
    r_index = (scheduled_key[rc4_prga.x] + scheduled_key[rc4_prga.y]) % 256
    return scheduled_key[r_index]


def rc4_ksa(byte_key):
    s_arr = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s_arr[i] + byte_key[i % len(byte_key)]) % 256
        s_arr[i], s_arr[j] = s_arr[j], s_arr[i]
    return s_arr


def rc4_processing(data, byte_key, encrypt):
    cyphered_bytes = bytearray()
    scheduled_key = rc4_ksa(byte_key)
    rc4_prga.x = 0
    rc4_prga.y = 0

    for byte in data:
        cyphered_bytes.append(byte ^ rc4_prga(scheduled_key))
    if encrypt == "encrypt":
        result_str = cyphered_bytes
    else:
        result_str = cyphered_bytes.decode("utf-8")
    return result_str


@crypto_tools.file_manipulation()
def rc4(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")
    byte_key = bytearray(key, "utf-8")
    if len(byte_key) > 256:
        raise ValueError("Key len must be <= 256")
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    return rc4_processing(data, byte_key, encrypt)


rc4.little_doc = rc4_little_doc
rc4.full_doc = rc4_full_doc
