import crypto_tools


def hash(data):
    if data.__class__ == str:
        data_in_bytes = bytearray(data, "utf-8")
    return "Hello world"
