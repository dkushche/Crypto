from json import load as get_json

"""
    In this file we have some general tools
    for crypto algorithms
"""


def supl_to_mult(first_len, second_len, data):
    if first_len > second_len:
        need_to_add = first_len % second_len
    else:
        need_to_add = second_len - first_len
    for i in range(need_to_add):
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


def utf_decoder(data):
    if data.__class__ == bytes or data.__class__ == bytearray:
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
