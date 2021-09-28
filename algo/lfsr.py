import crypto_tools
from bitarray import bitarray
from math import ceil
import json


def lfsr_little_doc():
    return "Linear Feedback Shift Register"


def lfsr_full_doc():
    return """
    executive polynomial examples:
        [11, 2, 0], [30, 6, 4, 1, 0] [24, 4, 3, 1, 0]
    """

"""
Rewrite it using generator.
"""
def lfsr_tick(key):
    next_val = 0

    for val in key:
        next_val ^= val
    
    prev_bit = key[0]
    for i in range(1, len(key)):
        buf = key[i]
        key[i] = prev_bit
        prev_bit = buf

    key[0] = next_val

    return key


def key_from_poly(exec_poly):
    bytes_amount = ceil((max(exec_poly) + 1) / 8)
    key = bitarray()
    key.frombytes(bytes(bytes_amount))

    for val in exec_poly:
        key[len(key) - 1 - val] = 1

    return key

"""
Have no time refactor later
"""
def lfsr_processing(data, exec_poly):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    key = key_from_poly(exec_poly)

    result = bytearray()

    crypto_tools.supl_to_mult(data, len(bytes(key)))
    data_pos = 0
    key_pos = 0
    while data_pos != len(data):
        
        if key_pos == len(bytes(key)):
            key_pos = 0
            lfsr_tick(key)

        result.append(data[data_pos] ^ bytes(key)[key_pos])

        key_pos += 1
        data_pos += 1    

    return result


@crypto_tools.file_manipulation()
def lfsr(data):
    exec_poly = json.loads(crypto_tools.cterm('input', 'Enter executive polynomial(list): ', 'ans'))
    if exec_poly.__class__ != list:
        raise ValueError(f"Incorrect exec_poly class {exec_poly.__class__}")

    return lfsr_processing(data, exec_poly)


lfsr.little_doc = lfsr_little_doc
lfsr.full_doc = lfsr_full_doc
