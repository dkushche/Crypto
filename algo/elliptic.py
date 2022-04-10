""" Elliptic

Elliptic-curve cryptography(ECC) is an approach to
public-key cryptography based on the algebraic
structure of elliptic curves over finite fields.

Parameters
----------
TODO

Returns
-------
TODO

"""


import json
import crypto_tools


def elliptic_little_doc():
    return "encrypt/decrypt using elliptic algo"


def elliptic_full_doc():
    return """
    It's quite hard but I tried to write self documented so
    just try to read it and google some additional stuff
    """


def elliptic_encrypt(data, open_key, r_number, big_g):
    new_data = []
    for i in data:
        temp = big_g * ord(i)
        if not crypto_tools.elliptic_point.belong_to_curve(temp):
            crypto_tools.cterm(
                "output",
                f"Warning: {big_g} * {ord(i)} out of curve", "inf"
            )
        new_data.append(temp)
    crypto_tools.cterm("output", f"Encoded data = {new_data}", "inf")

    res_data = []
    for point in new_data:
        first_point = big_g * r_number
        second_point = point + open_key * r_number
        res_data.append(
            [[first_point.x, first_point.y], [second_point.x, second_point.y]]
        )

    return json.dumps(res_data)


def elliptic_decrypt(data, secret_key):
    cyphered_data = json.loads(data)
    result = []
    for cyphered_value in cyphered_data:
        first_point = crypto_tools.elliptic_point(
            cyphered_value[0][0], cyphered_value[0][1]
        )
        second_point = crypto_tools.elliptic_point(
            cyphered_value[1][0], cyphered_value[1][1]
        )

        cyphered_part = first_point * secret_key
        result.append(second_point - cyphered_part)
    return result


def elliptic_processing(data, elliptic_curve, g_value,
                        secret_key, r_number, encrypt):
    crypto_tools.elliptic_point.set_curve(*elliptic_curve)
    big_g = crypto_tools.elliptic_point(*g_value)
    open_key = big_g * secret_key
    if encrypt == "encrypt":
        return elliptic_encrypt(data, open_key, r_number, big_g)
    return elliptic_decrypt(data, secret_key)


@crypto_tools.file_manipulation()
def elliptic(data):
    data = crypto_tools.utf_decoder(data)

    elliptic_curve = crypto_tools.cterm('input',
                                        'Enter curve coefficients(a:b:p): ',
                                        'ans')
    elliptic_curve = crypto_tools.decode_params(elliptic_curve, 3)

    g_value = crypto_tools.cterm('input',
                                 'Enter generator point(x:y): ', 'ans')
    g_value = crypto_tools.decode_params(g_value, 2)

    secret_key = int(crypto_tools.cterm('input',
                                        'Enter secret key: ', 'ans'))
    r_number = int(crypto_tools.cterm('input',
                                      'Enter r number: ', 'ans'))

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if encrypt not in ("decrypt", "encrypt"):
        raise ValueError(f"Incorrect action {encrypt}")

    return elliptic_processing(data, elliptic_curve, g_value,
                               secret_key, r_number, encrypt)


elliptic.little_doc = elliptic_little_doc
elliptic.full_doc = elliptic_full_doc
