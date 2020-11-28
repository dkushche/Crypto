import crypto_tools


def diffie_hellman_little_doc():
    return "get full key with using Diffie-Hellman algorithm"


def diffie_hellman_full_doc():
    return """
    Just Diffie-Helman, easier then previous labs
    """


def diffie_hellman_processing(a_public_key, a_private_key,
                              b_public_key, b_private_key):
    a_partial_key = a_public_key ** a_private_key % b_public_key
    b_partial_key = a_public_key ** b_private_key % b_public_key

    a_full_key = b_partial_key ** a_private_key % b_public_key
    b_full_key = a_partial_key ** b_private_key % b_public_key

    if a_full_key == b_full_key:
        return a_full_key
    return f"Error: {a_full_key} != {b_full_key}"


@crypto_tools.file_manipulation(read_data=False)
def diffie_hellman():
    a_public_key = int(crypto_tools.cterm('input', 'Enter A public key: ', 'ans'))
    a_private_key = int(crypto_tools.cterm('input', 'Enter A private key: ', 'ans'))

    b_public_key = int(crypto_tools.cterm('input', 'Enter B public key: ', 'ans'))
    if not crypto_tools.is_prime(b_public_key):
        raise ValueError(f"B public key needs to be prime")
    b_private_key = int(crypto_tools.cterm('input', 'Enter B private key: ', 'ans'))

    if crypto_tools.EGCD(b_public_key, a_public_key)[0] != 1:
        raise ValueError("Public and private keys needs to be co-prime")

    return diffie_hellman_processing(a_public_key, a_private_key,
                                     b_public_key, b_private_key)


diffie_hellman.little_doc = diffie_hellman_little_doc
diffie_hellman.full_doc = diffie_hellman_full_doc

