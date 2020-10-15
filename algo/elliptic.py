import crypto_tools


def elliptic_little_doc():
    return "little_doc"


def elliptic_full_doc():
    return """
    full_doc
    """


def elliptic_processing(data, input_val):
    return data


@crypto_tools.file_manipulation
def elliptic(data):
    data = crypto_tools.utf_decoder(data)

    elliptic_curve = crypto_tools.cterm('input',
                                        'Enter curve coefficients(a:b): ', 'ans')
    # 4 * A^3 + 27 * B^2 mod p != 0
    g_value = int(crypto_tools.cterm('input',
                                     'Enter finite field(p) number: ', 'ans'))
    # P is prime and bigger then 3

    # Pm is decrypted data

    # K_value secret key 

    # We need some G with which we may culc Pa which open key: Pa = k * G
    x_value = int(crypto_tools.cterm('input',
                                     'Enter closed(x) number: ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError(f"Incorrect action {encrypt}")

    return elliptic_processing(data, input_val)


elliptic.little_doc = elliptic_little_doc
elliptic.full_doc = elliptic_full_doc
