import crypto_tools


def smart_shift(value, block_size):
    bits_amount = len("{0:b}".format(value))
    adder = 0
    if bits_amount == block_size:
        check_value = 1 << (bits_amount - 1)
        adder = (value & check_value) >> (bits_amount - 1)
    value = value << 1 + adder
    return value


def hash(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    result = bytearray(2)
    if len(data) % len(result):
        for i in range(len(data) % len(result)):
            data.append(0x00)
    dib_iter = 0
    while dib_iter < len(data):
        for res_iter in range(len(result)):
            result[res_iter] ^= data[dib_iter]
            dib_iter += 1
        integer = int.from_bytes(result, byteorder="big")
        integer = smart_shift(integer, len(result) * 8)
        result = bytearray(integer.to_bytes(3, byteorder="big")[1:3])
    return result
