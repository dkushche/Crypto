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
    crypto_tools.cterm("output", f"Hijacking using repeat cypher method", "inf")
    data_block_size = math.ceil(math.log2(open_mix))
    res_block_size = int(math.log2(open_mix))
    byte_buf = math.ceil(data_block_size / 8)

    block_val = crypto_tools.get_block_as_int(0, data_block_size, byte_buf, data)

    m_value = 1
    while ((block_val ** e_value ** m_value) % open_mix != block_val % open_mix):
        m_value += 1
    res_val = ((block_val ** e_value ** (m_value - 1)) % open_mix)

    return res_val


def rsa_hijack_chinese(data, open_mix, e_value):
    crypto_tools.cterm("output", f"Hijacking using chinese reminder method", "inf")
    return data

def rsa_hijack_nokey(data, open_mix, e_value):
    crypto_tools.cterm("output", f"Hijacking using nokey reading method", "inf")
    return data

@crypto_tools.file_manipulation
def rsa_hijack(data):
    data = crypto_tools.to_bitarray(data)

    method = crypto_tools.cterm('input',
                                'Enter hijack method(fermat|repeat|chinese|nokey): ', 'ans')

    open_mix = int(crypto_tools.cterm('input',
                                      'Enter open(p * q) number: ', 'ans'))
    e_value = int(crypto_tools.cterm('input',
                                     'Enter open(e) number: ', 'ans'))

    try:
        return getattr(sys.modules[__name__], "rsa_hijack_" + method)(data, open_mix, e_value)
    except AttributeError:
        raise ValueError(f"No such method: {method}")



rsa_hijack.little_doc = rsa_hijack_little_doc
rsa_hijack.full_doc = rsa_hijack_full_doc

