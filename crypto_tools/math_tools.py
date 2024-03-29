""" Math Tools

Some general math tools that can help with numbers)

"""

import math
import random


def EGCD(a, b):
    """
        Extended Euclidean algorithm
        computes common divisor of integers a and b.
        a * x + b * y = gcd(a, b)
        returns gcd, x, y or gcd, y, x.
        Sorry, I can't remember
    """
    if a == 0:
        return (b, 0, 1)

    b_div_a, b_mod_a = divmod(b, a)
    g, x, y = EGCD(b_mod_a, a)
    return (g, y - b_div_a * x, x)


def inverse_modulo_numb(determ, modulo):
    g, x, _ = EGCD(determ, modulo)
    if g != 1:
        return pow(determ, modulo - 2, modulo)

    return x % modulo


def is_perfect_square(num):
    if num <= 0:
        return False
    square = int(math.sqrt(num))
    return square ** 2 == num


def is_prime(num):
    if num < 0:
        raise ValueError(f"Can't check is prime negative value {num}")
    if num < 2 or num == 4:
        return False
    if num < 4:
        return True
    for i in range(2, num // 2):
        if num % i == 0:
            return False
    return True


def get_coprime(value):
    coprime = random.randint(2, value - 1)
    gcd, _, _ = EGCD(value, coprime)
    while gcd != 1:
        coprime = random.randint(2, value - 1)
        gcd, _, _ = EGCD(value, coprime)
    return coprime
