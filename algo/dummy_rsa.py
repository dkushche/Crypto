import crypto_tools


def dummy_rsa_little_doc():
    return "dummy_rsa it's super dummy rsa for easier analysis"


def dummy_rsa_full_doc():
    return """
    This rsa was created to facilitate implementation some
    of rsa_hijack tools. It can ONLY encrypt numbers
    """


def dummy_rsa_processing(data, p_value, q_value, e_value):
    if not (crypto_tools.is_prime(p_value) and crypto_tools.is_prime(q_value)):
        raise ValueError("P and Q value need to be prime")
    closed_euler = (p_value - 1) * (q_value - 1)
    gcd, _, _ = crypto_tools.EGCD(e_value, closed_euler)
    if gcd != 1:
        raise ValueError(f"GCD of E and P * Q == {gcd}")

    result = pow(data, e_value) % (p_value * q_value)

    return f"{result}"


@crypto_tools.file_manipulation
def dummy_rsa(data):
    data = int(crypto_tools.utf_decoder(data))
    e_value = int(crypto_tools.cterm('input',
                                     'Enter open(e) value: ', 'ans'))
    p_value = int(crypto_tools.cterm('input',
                                     'Enter first(p) number: ', 'ans'))
    q_value = int(crypto_tools.cterm('input',
                                     'Enter second(q) number: ', 'ans'))

    return dummy_rsa_processing(data, p_value, q_value, e_value)


dummy_rsa.little_doc = dummy_rsa_little_doc
dummy_rsa.full_doc = dummy_rsa_full_doc

