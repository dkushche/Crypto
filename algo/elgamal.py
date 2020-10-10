import crypto_tools
import random


def elgamal_little_doc():
    return "little_doc"


def elgamal_full_doc():
    return """
    full_doc
    """

def check_parameters(p_value, g_value, x_value):
    if not crypto_tools.is_prime(p_value):
        raise ValueError("P need to be prime")
    gcd, _, _ = crypto_tools.EGCD(p_value, g_value)
    if gcd != 1:
        raise ValueError(f"GCD of P and G == {gcd}")
    if x_value < 2 or x_value > p_value - 1:
        raise ValueError(f"With current params X must \
                           be in range [2; {p_value - 1}]")

@crypto_tools.check_time
def elgamal_processing(data, p_value, g_value, x_value):
    check_parameters(p_value, g_value, x_value)
    y_value = pow(g_value, x_value) % p_value
    k_value = crypto_tools.get_coprime(p_value - 1)
    return data


@crypto_tools.file_manipulation
def elgamal(data):
    p_value = int(crypto_tools.cterm('input',
                                     'Enter first(p) number: ', 'ans'))
    g_value = int(crypto_tools.cterm('input',
                                     'Enter generator(g) number: ', 'ans'))
    x_value = int(crypto_tools.cterm('input',
                                     'Enter closed(x) number: ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError(f"Incorrect action {encrypt}")

    return elgamal_processing(data, p_value, g_value, x_value)


elgamal.little_doc = elgamal_little_doc
elgamal.full_doc = elgamal_full_doc
