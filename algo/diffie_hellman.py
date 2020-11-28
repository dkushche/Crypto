import crypto_tools


def diffie_hellman_little_doc():
    return "get full key with using Diffie-Hellman algorithm"


def diffie_hellman_full_doc():
    return """
    Just Diffie-Helman scheme using rsa type and elliptic algorithm
    """

def elliptic_diffie_hellman_processing(a_private_key, b_private_key):
    elliptic_curve = crypto_tools.cterm('input',
                                        'Enter curve coefficients(a:b:p): ',
                                        'ans')
    elliptic_curve = crypto_tools.decode_params(elliptic_curve, 3)
    crypto_tools.elliptic_point.set_curve(*elliptic_curve)

    g_value = crypto_tools.cterm('input',
                                 'Enter generator point(x:y): ', 'ans')
    g_value = crypto_tools.decode_params(g_value, 2)
    G = crypto_tools.elliptic_point(*g_value)

    a_partial_key = G * a_private_key
    b_partial_key = G * b_private_key

    a_full_key = b_partial_key * a_private_key
    b_full_key = a_partial_key * b_private_key

    if a_full_key.x == b_full_key.x:
        return a_full_key.x
    return f"Error: {a_full_key.x} != {b_full_key.x}"


def rsa_diffie_hellman_processing(a_public_key, a_private_key,
                                  b_public_key, b_private_key):
    if not crypto_tools.is_prime(b_public_key):
        raise ValueError(f"B public key needs to be prime")
    if crypto_tools.EGCD(b_public_key, a_public_key)[0] != 1:
        raise ValueError("Public and private keys needs to be co-prime")

    a_partial_key = a_public_key ** a_private_key % b_public_key
    b_partial_key = a_public_key ** b_private_key % b_public_key

    a_full_key = b_partial_key ** a_private_key % b_public_key
    b_full_key = a_partial_key ** b_private_key % b_public_key

    if a_full_key == b_full_key:
        return a_full_key
    return f"Error: {a_full_key} != {b_full_key}"


@crypto_tools.file_manipulation(read_data=False)
def diffie_hellman():
    use_elliptic = crypto_tools.cterm('input', 'Use elliptic_algorithm(true/false): ', 'ans')
    if use_elliptic not in ["true", "false"]:
        raise ValueError(f"Incorrect answer {use_elliptic}")

    a_private_key = int(crypto_tools.cterm('input', 'Enter A private key: ', 'ans'))
    b_private_key = int(crypto_tools.cterm('input', 'Enter B private key: ', 'ans'))

    if use_elliptic == "true":
        return elliptic_diffie_hellman_processing(a_private_key, b_private_key)

    a_public_key = int(crypto_tools.cterm('input', 'Enter A public key: ', 'ans'))
    b_public_key = int(crypto_tools.cterm('input', 'Enter B public key: ', 'ans'))

    return rsa_diffie_hellman_processing(a_public_key, a_private_key,
                                         b_public_key, b_private_key)


diffie_hellman.little_doc = diffie_hellman_little_doc
diffie_hellman.full_doc = diffie_hellman_full_doc

