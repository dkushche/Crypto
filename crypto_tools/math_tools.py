def EGCD(a, b):
    """
        Extended Euclidean algorithm
        computes common divisor of integers a and b,
    """
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = EGCD(b_mod_a, a)
        return (g, y - b_div_a * x, x)


def inverse_modulo_numb(determ, modulo):
    gcd, alpha, beta = EGCD(determ, modulo)
    if abs(gcd) != 1:
        raise ValueError(f"Values aren't coprime integers gcd {gcd}")
    return alpha


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
