import crypto_tools


def diffie_hellman_little_doc():
    return "diffie_hellman_little_doc"


def diffie_hellman_full_doc():
    return """
    diffie_hellman_full_doc
    """


def diffie_hellman_processing(a_public_key, a_private_key,
                              b_public_key, b_private_key):
    return "Diffie"

@crypto_tools.file_manipulation(read_data=False)
def diffie_hellman():
    a_public_key = int(crypto_tools.cterm('input', 'Enter A public key: ', 'ans'))
    a_private_key = int(crypto_tools.cterm('input', 'Enter A private key: ', 'ans'))
    b_public_key = int(crypto_tools.cterm('input', 'Enter B public key: ', 'ans'))
    b_private_key = int(crypto_tools.cterm('input', 'Enter B private key: ', 'ans'))

    return diffie_hellman_processing(a_public_key, a_private_key,
                                     b_public_key, b_private_key)


diffie_hellman.little_doc = diffie_hellman_little_doc
diffie_hellman.full_doc = diffie_hellman_full_doc

