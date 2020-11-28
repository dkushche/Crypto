from bitarray import bitarray
import crypto_tools
import algo
import math
import sys


def rsa_hijack_little_doc():
    return "rsa_hijack_little_doc"


def rsa_hijack_full_doc():
    return """
    rsa_hijack_full_doc
    """


def check_params(open_mix, e_value):
    if open_mix <= 0 or e_value <= 0:
        raise("Open (p * q) and e_value must be > 0")
    if open_mix % 2 == 0:
        raise ("Open (p * q) must be odd")


@crypto_tools.check_time
def rsa_hijack_fermat(data, open_mix, e_value):
    data = crypto_tools.to_bitarray(data)
    crypto_tools.cterm("output", f"Hijacking using Fermat method", "inf")
    check_params(open_mix, e_value)
    k_value = 1

    a = int(math.sqrt(open_mix))
    b = a ** 2 - open_mix

    while(not crypto_tools.is_perfect_square(b)):
        a += 1
        b = a ** 2 - open_mix

    p_value = a + int(math.sqrt(b))
    q_value = a - int(math.sqrt(b))

    crypto_tools.cterm("output", f"P:Q = {p_value}:{q_value}", "inf")

    return algo.rsa.processor(data, p_value, q_value, e_value, "decrypt")


@crypto_tools.check_time
def rsa_hijack_repeat(data, open_mix, e_value):
    data = crypto_tools.to_bitarray(data)
    crypto_tools.cterm("output",
                       f"Hijacking using repeat cypher method", "inf")
    data_block_size = math.ceil(math.log2(open_mix))
    res_block_size = int(math.log2(open_mix))
    byte_buf = math.ceil(data_block_size / 8)

    block_val = crypto_tools.get_block_as_int(
        0, data_block_size, byte_buf, data
    )

    m_value = 1
    repeat_block = (block_val ** e_value ** m_value) % open_mix
    while (repeat_block != block_val % open_mix):
        m_value += 1
        repeat_block = (block_val ** e_value ** m_value) % open_mix
    res_val = ((block_val ** e_value ** (m_value - 1)) % open_mix)

    return res_val


@crypto_tools.check_time
def rsa_hijack_chinese(data, open_mix, e_value):
    data = int(crypto_tools.utf_decoder(data))
    crypto_tools.cterm("output",
                       f"Hijacking using chinese reminder method", "inf")

    tx_data = [data]
    open_mixes = [open_mix]

    for i in range(2, e_value + 1):
        tx_data.append(int(crypto_tools.utf_decoder(crypto_tools.get_data())))
        open_mixes.append(
            int(crypto_tools.cterm('input', f'Enter {i} open(p * q) number: ', 'ans')))

    result = 0
    m_value = 1
    for i in range(e_value):
        temp_m = 1
        m_value *= open_mixes[i]
        for j in range(1, e_value):
            temp_m *= open_mixes[(i + j) % e_value]

        inverse_m = crypto_tools.inverse_modulo_numb(temp_m, open_mixes[i])
        result += tx_data[i] * temp_m * inverse_m
    result = (result % m_value) ** (1 / float(e_value))
    return f"{result}"


@crypto_tools.check_time
def rsa_hijack_nokey(data, open_mix, e_value):
    data = int(crypto_tools.utf_decoder(data))
    crypto_tools.cterm("output",
                       f"Hijacking using nokey reading method", "inf")
    second_data = int(crypto_tools.utf_decoder(crypto_tools.get_data()))
    second_e_value = int(crypto_tools.cterm('input',
                                            'Enter second open(e) number: ', 'ans'))

    gcd, r, s = crypto_tools.EGCD(e_value, second_e_value)
    c1_r = pow(data, r) % open_mix
    c2_s = pow(crypto_tools.inverse_modulo_numb(second_data, open_mix), -s) % open_mix

    result = (c1_r * c2_s) % open_mix
    return f"{result}"


@crypto_tools.file_manipulation()
def rsa_hijack(data):
    method = crypto_tools.cterm(
        'input',
        'Enter hijack method(fermat|repeat|chinese|nokey): ',
        'ans'
    )

    open_mix = int(crypto_tools.cterm('input',
                                      'Enter open(p * q) number: ', 'ans'))
    e_value = int(crypto_tools.cterm('input',
                                     'Enter open(e) number: ', 'ans'))

    try:
        hijack = getattr(sys.modules[__name__], "rsa_hijack_" + method)
        return hijack(data, open_mix, e_value)
    except AttributeError:
        raise ValueError(f"No such method: {method}")


rsa_hijack.little_doc = rsa_hijack_little_doc
rsa_hijack.full_doc = rsa_hijack_full_doc
