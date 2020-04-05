import crypto_tools


def smart_shift(value):
    bits_amount = len("{0:b}".format(value))
    adder = 0
    if bits_amount == 8:
        check_value = 1 << (bits_amount - 1)
        adder = (value & check_value) >> (bits_amount - 1)
    value = value << 1
    return value, adder


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

        last_excess = 0
        for res_iter in range(len(result) - 1, -1, -1):
            integer, new_excess = smart_shift(result[res_iter])
            integer += last_excess
            last_excess = new_excess
            byte_arr = integer.to_bytes(2, byteorder="big")
            byte_arr = byte_arr[-1]
            result[res_iter] = byte_arr
            if res_iter == 0:
                result[len(result) - 1] += last_excess
    return result
