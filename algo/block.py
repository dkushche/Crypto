import crypto_tools
from .xor import xor_processing


def block_little_doc():
    return "encrypt/decrypt using block cypher"


def block_full_doc():
    return """
    The easiest block algorithm check th wiki
    """


def secret_crypto_func(val, now_round, key, block_size):
    key_start = now_round * block_size
    key_end = key_start + block_size
    secret_val = xor_processing(val, key[key_start: key_end], "encrypt")
    return secret_val


def block_pre_processing(data, key, block_size, rounds):
    if data.__class__ == str:
        data = bytearray(data.encode())
    if key.__class__ == str:
        key = bytearray(key.encode())

    if len(key) > (block_size * rounds):
        raise ValueError("Too big key. Max len required: block_size * rounds")
    else:
        crypto_tools.supl_to_mult(key, block_size * rounds)

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

    for left, right in crypto_tools.block_generator(data, block_size):

        left, right = crypto_tools.feistel_network(left, right, encrypt, rounds,
                                                   True, xor_processing,
                                                   secret_crypto_func, key, block_size)

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
