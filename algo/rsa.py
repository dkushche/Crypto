""" RSA

RSA (Rivest–Shamir–Adleman) is a public-key cryptosystem that is widely used
for secure data transmission. It is also one of the oldest. The acronym "RSA"
comes from the surnames of Ron Rivest, Adi Shamir and Leonard Adleman, who
publicly described the algorithm in 1977. An equivalent system was developed
secretly in 1973 at GCHQ (the British signals intelligence agency) by the English
mathematician Clifford Cocks. That system was declassified in 1997.

Parameters
----------
TODO

Returns
-------
TODO

"""

import math
from bitarray import bitarray
import crypto_tools


def rsa_little_doc():
    return "encrypt/decrypt using rsa algo"


def rsa_full_doc():
    return """
        RSA quite easy, but still effective and elegant;
        I love it. Block size in bits
    """


def get_closed_key(p_value, q_value, e_value):
    if not (crypto_tools.is_prime(p_value) and crypto_tools.is_prime(q_value)):
        raise ValueError("P and Q value need to be prime")
    closed_euler = (p_value - 1) * (q_value - 1)
    gcd, _, _ = crypto_tools.EGCD(e_value, closed_euler)
    if gcd != 1:
        raise ValueError(f"GCD of E and P * Q == {gcd}")
    m_value = 1
    d_value = (m_value * closed_euler + 1) / e_value
    while not d_value.is_integer():
        m_value += 1
        d_value = (m_value * closed_euler + 1) / e_value

    return int(d_value)


def get_block_sizes(encrypt, encrypt_block_size, decrypt_block_size):
    if encrypt == "encrypt":
        data_block_size = encrypt_block_size
        res_block_size = decrypt_block_size
    else:
        data_block_size = decrypt_block_size
        res_block_size = encrypt_block_size
    return data_block_size, res_block_size


def rsa_processing(data, p_value, q_value, e_value, encrypt):
    open_mix = p_value * q_value
    d_value = get_closed_key(p_value, q_value, e_value)
    encrypt_block_size = int(math.log2(open_mix))
    decrypt_block_size = math.ceil(math.log2(open_mix))
    byte_buf = math.ceil(decrypt_block_size / 8)

    data_block_size, res_block_size = get_block_sizes(
        encrypt, encrypt_block_size, decrypt_block_size
    )
    key = e_value if encrypt == "encrypt" else d_value
    crypto_tools.supl_to_mult(data, data_block_size)

    result = bitarray()
    for i in range(0, len(data), data_block_size):
        block_val = crypto_tools.get_block_as_int(
            i, data_block_size, byte_buf, data
        )
        crypto_tools.cterm(
            "output", f"Block {int(i / data_block_size)}: {block_val}", "inf"
        )

        res_val = (pow(block_val, key) % open_mix).to_bytes(byte_buf, "big")

        block = crypto_tools.to_bitarray(res_val)
        result += block[-res_block_size:]

    if encrypt == "decrypt":
        if len(result) % 8:
            result = result[:-(len(result) % 8)]
    result = bytes(result)
    return result if encrypt == "encrypt" else result.decode()


@crypto_tools.file_manipulation()
def rsa(data):
    data = crypto_tools.to_bitarray(data)

    p_value = int(crypto_tools.cterm('input',
                                     'Enter first(p) number: ', 'ans'))
    q_value = int(crypto_tools.cterm('input',
                                     'Enter second(q) number: ', 'ans'))
    e_value = int(crypto_tools.cterm('input',
                                     'Enter open(e) number: ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError(f"Incorrect action {encrypt}")
    return rsa_processing(data, p_value, q_value, e_value, encrypt)


rsa.little_doc = rsa_little_doc
rsa.full_doc = rsa_full_doc
rsa.processor = rsa_processing
