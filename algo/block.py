import crypto_tools


"""
    data: user input
    key: data in bits
    rounds: amount of rounds
    func: secret crypto function
"""


def secret_crypto_func(val, key, now_round):
    return (val + key + now_round) % 256


def set_rounds_range(encrypt, rounds):
    if encrypt == "encrypt":
        return 0, rounds, 1
    else:
        return rounds - 1, -1, -1


def feistel_network(left, right, key, encrypt, rounds):
    min_lim, max_lim, step = set_rounds_range(encrypt, rounds)
    for now_round in range(min_lim, max_lim, step):
        buf = right ^ secret_crypto_func(left, key, now_round)
        if (now_round != max_lim - 1):
            right = left
            left = buf
        else:
            right = buf
    return left, right


def block(data, key, rounds, func, encrypt):
    """
        For now we use something very easy
        like 16 bit block and modulo func
    """
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    data = bytearray(data) #I'm not sure about it, but let it be
    if (len(data) % 2):
        data.append(0x00)
    for i in range(0, len(data), 2):
        data[i], data[i + 1] = feistel_network( data[i], data[i + 1],
                                                key, encrypt, rounds)
    if encrypt == "encrypt":
        result_str = data
    else:
        result_str = data.decode("utf-8")
    return result_str