import crypto_tools
import math


def rsa_little_doc():
    return "encrypt/decrypt using rsa algo"


def rsa_full_doc():
    return """
        RSA quite easy, but still effective and elegant;
        I love it.
    """


def rsa_processing(data, p_value, q_value, e_value, m_value, encrypt):
    if crypto_tools.is_prime(p_value) and crypto_tools.is_prime(q_value):
        open_mix = p_value * q_value
        closed_euler = (p_value - 1) * (q_value - 1)
        gcd, _, _ = crypto_tools.EGCD(e_value, closed_euler)
        if gcd != 1:
            raise ValueError(f"GCD of E and P * Q == {gcd}")
        d_value = (m_value * closed_euler + 1) // e_value
        block_size = int(math.log2(open_mix))
        if block_size // 8 < 1:
            raise ValueError(f"P * Q needs to be bigger 2^8 but it {open_mix}")
        crypto_tools.supl_to_mult(data, block_size)
        key = e_value if encrypt == "encrypt" else d_value
        result = bytearray()
        for i in range(0, len(data), block_size // 8):
            block_val = int.from_bytes(data[i: i + block_size // 8], "big")
            assert 0 <= block_val < pow(2, block_size) - 1
            result += (pow(block_val, key) % open_mix).to_bytes(
                        block_size // 8, "big")
        if encrypt == "encrypt":
            return result
        else:
            return result.decode()
    else:
        raise ValueError("P and Q value need to be prime")
    return result


@crypto_tools.file_manipulation
def rsa(data):
    if data.__class__ == str:
        data = bytearray(data.encode())
    p_value = int(crypto_tools.cterm('input',
                                     'Enter first(p) number: ', 'ans'))
    q_value = int(crypto_tools.cterm('input',
                                     'Enter second(q) number: ', 'ans'))
    e_value = int(crypto_tools.cterm('input',
                                     'Enter open(e) number: ', 'ans'))
    m_value = int(crypto_tools.cterm('input',
                                     'Enter multiplier(M) number: ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError(f"Incorrect action {encrypt}")
    return rsa_processing(data, p_value, q_value, e_value, m_value, encrypt)


rsa.little_doc = rsa_little_doc
rsa.full_doc = rsa_full_doc
