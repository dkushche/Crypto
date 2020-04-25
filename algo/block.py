import crypto_tools


def block_proccess_input(data, encrypt):
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    if (len(data) % 2):
        data.append(0x00)
    return data


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
        if (now_round != max_lim - step):
            right = left
            left = buf
        else:
            right = buf
    return left, right


def block(data, key, rounds, func, encrypt):
    """
        data: user input
        key: data in bits
        rounds: amount of rounds
        func: secret crypto function
    """

    data = block_proccess_input(data, encrypt)
    res_data = bytearray()
    data_iter = iter(data)
    for val in data_iter:
        left, right = feistel_network(val, next(data_iter),
                                      key, encrypt, rounds)
        res_data.append(left)
        res_data.append(right)
    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode("utf-8")
    return result_str
