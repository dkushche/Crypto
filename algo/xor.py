from itertools import cycle

def xor(data, key):
    key_bytes = cycle(bytearray(key, "utf-8"))
    data_in_bytes = bytearray(data, "utf-8")
    result_bytes = bytearray(a ^ b for a, b in zip(data_in_bytes, key_bytes))
    result_str = result_bytes.decode("utf-8")
    return result_str

def hack_xor(data):
    print("Error: You can't hack this algo")
    return None
