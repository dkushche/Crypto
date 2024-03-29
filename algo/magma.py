""" Magma

The GOST block cipher (Magma), defined in the standard GOST 28147-89 (RFC 5830),
is a Soviet and Russian government standard symmetric key block cipher with a
block size of 64 bits. The original standard, published in 1989, did not give
the cipher any name, but the most recent revision of the standard, GOST R
34.12-2015 (RFC 7801, RFC 8891), specifies that it may be referred to as Magma.
The GOST hash function is based on this cipher. The new standard also specifies
a new 128-bit block cipher called Kuznyechik.

Parameters
----------
TODO

Returns
-------
TODO

"""

from math import ceil
from bitarray import bitarray
import crypto_tools
from .xor import xor_processing
from .lfsr_generator import lfsr_generator_processing


def magma_little_doc():
    return "block algorithm ГОСТ 28147-89"


def magma_full_doc():
    return """
    https://spy-soft.net/magma-encryption/
    """


def magma_secret_func(val, now_round, block_size, key):
    del block_size

    sub_key_table = [ 0, 1, 2, 3, 4, 5, 6, 7,
                      0, 1, 2, 3, 4, 5, 6, 7,
                      0, 1, 2, 3, 4, 5, 6, 7,
                      7, 6, 5, 4, 3, 2, 1, 0 ]

    t_table = [
        [ 1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2 ],
        [ 8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7 ],
        [ 5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0 ],
        [ 7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12 ],
        [ 12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11 ],
        [ 11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0 ],
        [ 6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15 ],
        [ 12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1 ]
    ]

    sub_key = key[sub_key_table[now_round]:sub_key_table[now_round] + 4: 1]

    stage_1 = (int.from_bytes(val, byteorder="big") +
                int.from_bytes(sub_key, byteorder="big")) % 32

    stage_2 = bitarray()

    for part_id in range(4):
        first_part_byte = t_table[part_id * 2][stage_1 & 0xF0 >> 4]
        sec_part_byte = t_table[part_id * 2 + 1][stage_1 & 0x0F]

        first_part_byte = crypto_tools.to_bitarray(first_part_byte.to_bytes(1, 'big'))[4:8]
        sec_part_byte = crypto_tools.to_bitarray(sec_part_byte.to_bytes(1, 'big'))[4:8]

        stage_2 += first_part_byte + sec_part_byte

    temp = stage_2[0:11]
    stage_3 = stage_2[11:32]
    stage_3.append(temp)

    return bytes(stage_3)


def magma_pre_processing(data, key, key_len):
    if data.__class__ == str:
        data = bytearray(data.encode())
    if key.__class__ == str:
        key = bytearray(key.encode())

    if len(key) > key_len:
        raise ValueError(f"Too big key. Max len required: {key_len}")
    crypto_tools.supl_to_mult(key, key_len)

    return data, key


def magma_processing(data, key, encrypt, mode):
    block_size = 8
    rounds = 32
    key_len = 32

    data, key = magma_pre_processing(data, key, key_len)

    res_data = None

    if mode == "xor":
        synchro_package = lfsr_generator_processing(2, [3, 5, 6, 7, 9, 14], [2, 4, 5, 7],
                                                    ceil(len(data) / block_size) * block_size)

        crypto_tools.supl_to_mult(data, block_size)

        synchro_package_stage_1 = crypto_tools.block_cypher(synchro_package, block_size,
                                                            "encrypt", rounds, False,
                                                            xor_processing, magma_secret_func, key)

        synchro_package_stage_2 = bytearray()

        for block_id in range(len(synchro_package_stage_1) // 8):
            first_start = block_id * 8
            second_start = first_start + block_size // 2

            first_part = synchro_package_stage_1[first_start:first_start + block_size // 2]
            second_part = synchro_package_stage_1[second_start:second_start + block_size // 2]

            const_0 = 0x1010101
            const_1 = 0x1010104

            first_part = (int.from_bytes(first_part, byteorder="big") + const_0) % pow(2, 32)
            second_part = (int.from_bytes(second_part, byteorder="big") +
                          const_1 - 1) % pow(2, 32 - 1) + 1

            synchro_package_stage_2 += first_part.to_bytes(4, 'big') +\
                                       second_part.to_bytes(4, 'big')

        synchro_package_stage_3 = crypto_tools.block_cypher(
            synchro_package_stage_2,block_size, "encrypt", rounds,
            False, xor_processing, magma_secret_func, key
        )

        res_data = xor_processing(data, synchro_package_stage_3, "encrypt")
    else:
        res_data  = crypto_tools.block_cypher(data, block_size, encrypt, rounds,
                                              False, xor_processing, magma_secret_func, key)

    return res_data


@crypto_tools.file_manipulation()
def magma(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError("Incorrect type")

    mode = crypto_tools.cterm(
        'input',
        'Enter mode(simple_replacement|xor): ',
        'ans'
    )

    if mode not in ["simple_replacement", "xor"]:
        raise ValueError(f"Incorrect mode: {mode}")

    res_data =  magma_processing(data, key, encrypt, mode)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


magma.little_doc = magma_little_doc
magma.full_doc = magma_full_doc
