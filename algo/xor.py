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
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError("Incorrect action")
    if len(key) == 0:
        raise ValueError("Empty key")
    if key.__class__ == str:
        key = bytearray(key, "utf-8")
    return xor_processing(data, key, encrypt)


xor.little_doc = xor_little_doc
xor.full_doc = xor_full_doc
