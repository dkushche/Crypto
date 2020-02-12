from itertools import cycle


def xor(data, key, encrypt):
    if encrypt != "encrypt" and encrypt != "decrypt":
        print("Incorrect type")
        raise ValueError
    if len(key) == 0:
        print("Empty key")
        raise ValueError
    key_bytes = cycle(bytearray(key, "utf-8"))
    if encrypt == "encrypt":
        data_in_bytes = bytearray(data, "utf-8")
    else:
        data_in_bytes = data
    result_bytes = bytearray(a ^ b for a, b in zip(data_in_bytes, key_bytes))
    if encrypt == "encrypt":
        result_str = result_bytes
    else:
        result_str = result_bytes.decode("utf-8")
    return result_str


def hack_xor(data):
    print("Error: You can't hack this algo")
    raise FileNotFoundError
