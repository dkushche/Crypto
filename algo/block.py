import crypto_tools
from .xor import xor

def block_proccess_input(data, key, block_size, rounds, encrypt):
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")

    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    if key.__class__ == str:
        key = bytearray(key, "utf-8")

    if block_size < 2 or block_size % 2:
        ValueError("Block size must be bigger then 1 and be pair")
    if rounds < 1:
        ValueError("You need enter more then 0 rounds")

    if len(key) > (block_size * rounds):
        ValueError("Too big key max len of key needs to be block_size * rounds")
    else:
        crypto_tools.supl_to_mult(len(key), block_size * rounds, key)
    crypto_tools.supl_to_mult(len(data), block_size, data)
    return data, key


def secret_crypto_func(val, key, block_size, now_round):
    key_start = now_round * block_size
    key_end = key_start + block_size
    secret_val = xor(val, key[key_start: key_end], "encrypt")
    return secret_val


def set_rounds_range(encrypt, rounds):
    if encrypt == "encrypt":
        return 0, rounds, 1
    else:
        return rounds - 1, -1, -1


def feistel_network(left, right, block_size, key, encrypt, rounds):
    min_lim, max_lim, step = set_rounds_range(encrypt, rounds)
    for now_round in range(min_lim, max_lim, step):
        buf = xor(right, secret_crypto_func(left, key, block_size, now_round), "encrypt")
        if (now_round != max_lim - step):
            right = left
            left = buf
        else:
            right = buf
    return left, right


def block(data, key, block_size, rounds, encrypt):
    """
        data: user input
        block_size: size of block
        key: data in bits(key size = block_size * rounds)
        rounds: amount of rounds
    """

    data, key = block_proccess_input(data, key, block_size, rounds, encrypt)
    res_data = bytearray()
    for block_id in range(len(data) // block_size):
        left_start = block_id * block_size
        left_end = left_start + (block_size // 2)
        left = data[left_start:left_end:1]

        right_start = left_end
        right_end = right_start + (block_size // 2)
        right = data[right_start:right_end:1]

        left, right = feistel_network(left, right, block_size,
                                      key, encrypt, rounds)

        for byte in left:
            res_data.append(byte)
        for byte in right:
            res_data.append(byte)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode("utf-8")
    return result_str
