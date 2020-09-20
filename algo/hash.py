import crypto_tools


def hash_little_doc():
    return "generate hash from data"


def hash_full_doc():
    return """
    Basic hash algorithm that uses xor
    """


def smart_shift(value, block_size):
    bits_amount = len("{0:b}".format(value))
    adder = 0
    if bits_amount == block_size:
        check_value = 1 << (bits_amount - 1)
        adder = (value & check_value) >> (bits_amount - 1)
    value <<= 1
    return value + adder


def hash_processing(data, res_size):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    result = bytearray(res_size)
    crypto_tools.supl_to_mult(len(data), len(result), data)
    dib_iter = 0

    while dib_iter < len(data):
        for res_iter in range(len(result)):
            result[res_iter] ^= data[dib_iter]
            dib_iter += 1
        integer = int.from_bytes(result, byteorder="big")
        integer = smart_shift(integer, len(result) * 8)
        result = bytearray(integer.to_bytes(res_size + 1,
                           byteorder="big")[1:res_size + 1])
    return result


@crypto_tools.file_manipulation
def hash(data):
    res_size = int(crypto_tools.cterm('input',
                                      'Size of result(in bytes): ', 'ans'))
    return hash_processing(data, res_size)


hash.little_doc = hash_little_doc
hash.full_doc = hash_full_doc
