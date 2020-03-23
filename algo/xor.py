from itertools import cycle


def xor(data, key, encrypt):
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError("Incorrect action")
    if len(key) == 0:
        raise ValueError("Empty key")
    key_bytes = cycle(bytearray(key, "utf-8"))
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
