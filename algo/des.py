""" DES

Data Encryption Standard is the archetypal block cipher—an algorithm that
takes a fixed-length string of plaintext bits and transforms it through a
series of complicated operations into another ciphertext bitstring
of the same length

Parameters
----------
TODO

Returns
-------
TODO

"""

from bitarray import bitarray

import crypto_tools
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


def s_table_permutation(xor_with_key):
    s_table = [
        [
            [ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 ],
            [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 ],
            [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 ],
            [ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]
        ],
        [
            [ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 ],
            [ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 ],
            [ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 ],
            [ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]
        ],
        [
            [ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 ],
            [ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 ],
            [ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 ],
            [ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]
        ],
        [
            [ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15 ],
            [ 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9 ],
            [ 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4 ],
            [ 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ]
        ],
        [
            [ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9 ],
            [ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6 ],
            [ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14 ],
            [ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]
        ],
        [
            [ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11 ],
            [ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8 ],
            [ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6 ],
            [ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ]
        ],
        [
            [ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1 ],
            [ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6 ],
            [ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2 ],
            [ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 ]
        ],
        [
            [ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7 ],
            [ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2 ],
            [ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8 ],
            [ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 ]
        ]
    ]

    after_s = bitarray()
    xor_with_key_bit = crypto_tools.to_bitarray(bytes(xor_with_key))
    for i in range(0, len(xor_with_key_bit), 6):
        xwk_part = xor_with_key_bit[i:i + 6]
        val_a = bitarray([xwk_part[0], xwk_part[-1]])
        val_b = xwk_part[1:5]

        res_part = crypto_tools.to_bitarray(
            (
                s_table[i // 6][int(val_a.to01(), 2)][int(val_b.to01(), 2)]
            ).to_bytes(1, byteorder='big')
        )[4:]

        after_s += res_part

    return bytes(after_s)


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

    after_s = s_table_permutation(xor_with_key)

    p_permutation = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]

    result = crypto_tools.permutation_by_table(
        p_permutation, after_s, len(after_s)
    )

    return result


def des_pre_processing(key):
    if len(key) > 7:
        raise ValueError("Too big key. Max len required: 7")

    crypto_tools.supl_to_mult(key, 7)


def des_processing(data, key, encrypt):
    block_size = 8
    rounds = 16

    des_pre_processing(key)
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
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    res_data = des_processing(data, key, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


des.little_doc = des_little_doc
des.full_doc = des_full_doc
