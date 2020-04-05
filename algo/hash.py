import crypto_tools


def smart_shift(value):
    bits_amount = len("{0:b}".format(value))
    adder = 0
    if bits_amount == 8:
        check_value = 1 << (bits_amount - 1)
        adder = (value & check_value) >> (bits_amount - 1)
    value = value << 1 + adder
    return value


def hash(data):
    if data.__class__ == str:
        data_in_bytes = bytearray(data, "utf-8")
    result = bytearray(2)
    if len(data_in_bytes) % len(result):
        for i in range(len(data_in_bytes) % len(result)):
            data_in_bytes.append(0x00)
    dib_iter = 0
    while dib_iter < len(data_in_bytes):
        for res_iter in range(len(result)):
            result[res_iter] ^= data_in_bytes[dib_iter]
            integer = smart_shift(result[res_iter])
            byte_arr = integer.to_bytes(2, byteorder="big")
            byte_arr = byte_arr[-1]
            result[res_iter] = byte_arr
            dib_iter += 1
    print(bytes(result))
    return result
