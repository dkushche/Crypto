import crypto_tools
from bitarray import bitarray
from .xor import xor_processing


def des_little_doc():
    return "des_little_doc"


def des_full_doc():
    return """
    des_full_doc
    """


def key_extension(key):
    key_in_bits = crypto_tools.to_bitarray(bytes(key))
    extended_key = bitarray()

    for idx in range(0, len(key_in_bits), 7):
        part = key_in_bits[idx:idx + 7]

        if part.count("1") % 2 == 0:
            part += bitarray('1')
        else:
            part += bitarray('0')

        extended_key += part

    key_mutation_table = [
        57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
    ]

    extended_key = crypto_tools.permutation_by_table(
        key_mutation_table, extended_key, len(extended_key)
    )

    return bytes(extended_key)


def des_secret_func(val, now_round, block_size, extended_key):
    extension_table = [
        32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    val = crypto_tools.permutation_by_table(
        extension_table, val, int(block_size / 2)
    )

    round_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    shifted_key = extended_key[round_shifts[now_round]:] + extended_key[:round_shifts[now_round]]

    key_regression_table = [
        14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10, 23, 19, 12, 4,
        26, 8,  16, 7,  27, 20, 13, 2,  41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    ]

    round_key = crypto_tools.permutation_by_table(
        key_regression_table, shifted_key, len(shifted_key)
    )

    xor_with_key = xor_processing(val, round_key, "encrypt")

    return xor_with_key


def des_pre_processing(data, key):
    if len(key) > 7:
        raise ValueError(f"Too big key. Max len required: 7")
    else:
        crypto_tools.supl_to_mult(key, 7)


def des_processing(data, key, encrypt):
    block_size = 8
    rounds = 16

    des_pre_processing(data, key)
    if encrypt == "encrypt":
        start_permutation_table = [
            58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
        ]

        data = crypto_tools.permutation_by_table(
            start_permutation_table, data, block_size
        )

    extended_key = key_extension(key)

    res_data = crypto_tools.block_cypher(data, block_size, encrypt, rounds,
                                         False, xor_processing, des_secret_func, extended_key)

    if encrypt == "decrypt":
        start_permutation_table = [
            40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9,  49, 17, 57, 25
        ]

        res_data = crypto_tools.permutation_by_table(
            start_permutation_table, res_data, block_size
        )

    return res_data


@crypto_tools.file_manipulation()
def des(data):
    if data.__class__ == str:
        data = bytearray(data.encode())

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")

    res_data = des_processing(data, key, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


des.little_doc = des_little_doc
des.full_doc = des_full_doc
