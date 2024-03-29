""" Block cypher tools

Set of tools for creating standart block
cyphers based on Feistel Network

"""

from bitarray import bitarray
from .general_tools import supl_to_mult
from .general_tools import to_bitarray


def block_generator(data, block_size):
    if block_size < 2 or block_size % 2:
        raise ValueError("Block size must be bigger then 1 and be pair")

    supl_to_mult(data, block_size)

    for block_id in range(len(data) // block_size):
        left_start = block_id * block_size
        left_end = left_start + (block_size // 2)
        left = data[left_start:left_end:1]

        right_start = left_end
        right_end = right_start + (block_size // 2)
        right = data[right_start:right_end:1]

        yield left, right


def permutation_by_table(table, data, block_size):
    supl_to_mult(data, block_size)
    result = bitarray()

    for idx in range(0, len(data), block_size):
        block = data[idx:idx + block_size]
        block_in_bits = to_bitarray(bytes(block))
        result_block = bitarray([block_in_bits[i - 1] for i in table])
        result += result_block

    return bytes(result)


def set_rounds_range(encrypt, rounds):
    if encrypt == "encrypt":
        return 0, rounds, 1
    return rounds - 1, -1, -1


def feistel_network(left, right, encrypt, rounds, left_xor,
                    xor_func, secret_function, block_size, *args):
    if rounds < 1:
        raise ValueError("You need enter more then 0 rounds")

    if left_xor is False:
        left, right = right, left

    min_lim, max_lim, step = set_rounds_range(encrypt, rounds)
    for now_round in range(min_lim, max_lim, step):
        secret_val = secret_function(left, now_round, block_size, *args)
        buf = xor_func(right, secret_val, "encrypt")
        if now_round != max_lim - step:
            right = left
            left = buf
        else:
            right = buf
    if left_xor is False:
        return right, left
    return left, right


def block_cypher(data, block_size, encrypt, rounds,
                 left_xor, xor_processing, secret_crypto_func, *args):
    res_data = bytearray()

    for left, right in block_generator(data, block_size):
        left, right = feistel_network(left, right, encrypt, rounds,
                                      left_xor, xor_processing,
                                      secret_crypto_func, block_size, *args)

        for byte in left:
            res_data.append(byte)
        for byte in right:
            res_data.append(byte)

    return res_data
