""" General Tools

Here we have some general tools
for crypto algorithms

"""

from bitarray import bitarray

def supl_to_mult(data, mod_len):
    if len(data) % mod_len:
        if len(data) > mod_len:
            buf = mod_len - (len(data) % mod_len)
        else:
            buf = mod_len - len(data)
        for _ in range(buf):
            data.append(0x00)


def bytes_to_str(bytes_arr):
    """
        This function print all bytes in the same
        way as C/C++. When we have 2 in python we get 10,
        but I want to see it as like 00000010
    """
    res_str = ""
    for byte in bytes_arr:
        byte_str = "{0:b}".format(byte)
        res_str += "0" * (8 - len(byte_str))
        res_str += byte_str
    return res_str


def get_block_as_int(start, src_bit_len, dst_byte_len, src):
    block = bitarray()
    block += bitarray('0') * (dst_byte_len * 8 - src_bit_len)
    block += src[start: start + src_bit_len]

    block_val = int.from_bytes(block, "big")
    return block_val


def decode_params(string, needed_size):
    result = string.split(":")
    if len(result) != needed_size:
        raise ValueError(
            f"Incorrect amount of params {len(result)}(need {needed_size})"
        )
    for i in range(len(result)):
        result[i] = int(result[i])
    return result


def to_bitarray(data):
    result = bitarray()
    if data.__class__ == str:
        result.frombytes(data.encode())
    elif data.__class__ in (bytearray, bytes):
        result.frombytes(data)
    else:
        raise ValueError(f"to_bits: incorrect data type {data.__class__}")
    return result


def utf_decoder(data):
    if data.__class__ in (bytearray, bytes):
        data = data.decode("utf-8")
    return data


def is_string_reproduced(templates, result):
    """
        Check does any word from dictionary
        in resulting string
    """
    for template in templates:
        if template in result:
            return True
    return False
