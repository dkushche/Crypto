import crypto_tools
from .xor import xor_processing


def block_little_doc():
    return "encrypt/decrypt using block cypher"


def block_full_doc():
    return """
    The easiest block algorithm check th wiki
    """


def secret_crypto_func(val, key, block_size, now_round):
    key_start = now_round * block_size
    key_end = key_start + block_size
    secret_val = xor_processing(val, key[key_start: key_end], "encrypt")
    return secret_val


def set_rounds_range(encrypt, rounds):
    if encrypt == "encrypt":
        return 0, rounds, 1
    else:
        return rounds - 1, -1, -1


def feistel_network(left, right, block_size, key, encrypt, rounds):
    min_lim, max_lim, step = set_rounds_range(encrypt, rounds)
    for now_round in range(min_lim, max_lim, step):
        secret_val = secret_crypto_func(left, key, block_size, now_round)
        buf = xor_processing(right, secret_val, "encrypt")
        if (now_round != max_lim - step):
            right = left
            left = buf
        else:
            right = buf
    return left, right


def block_pre_processing(data, key, block_size, rounds):
    if data.__class__ == str:
        data = bytearray(data.encode())
    if key.__class__ == str:
        key = bytearray(key.encode())

    if block_size < 2 or block_size % 2:
        raise ValueError("Block size must be bigger then 1 and be pair")
    if rounds < 1:
        raise ValueError("You need enter more then 0 rounds")

    if len(key) > (block_size * rounds):
        raise ValueError("Too big key. Max len required: block_size * rounds")
    else:
        crypto_tools.supl_to_mult(key, block_size * rounds)
    crypto_tools.supl_to_mult(data, block_size)
    return data, key


def block_processing(data, key, block_size, rounds, encrypt):
    """
        data: user input
        block_size: size of block
        key: data in bits(key size = block_size * rounds)
        rounds: amount of rounds
    """

    data, key = block_pre_processing(data, key, block_size, rounds)
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
        result_str = res_data.decode()
    return result_str


@crypto_tools.file_manipulation()
def block(data):
    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    block_size = int(crypto_tools.cterm('input', 'Block size(int): ', 'ans'))
    rounds = int(crypto_tools.cterm('input', 'Rounds(int): ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")
    return block_processing(data, key, block_size, rounds, encrypt)


block.little_doc = block_little_doc
block.full_doc = block_full_doc
