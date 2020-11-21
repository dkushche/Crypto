import crypto_tools


def dsa_little_doc():
    return "dsa_little_doc"


def dsa_full_doc():
    return """
    dsa_full_doc
    """


def check_params(p_value, q_value):
    if not crypto_tools.is_prime(p_value):
        raise ValueError(f"P({p_value}) is not prime")
    if not crypto_tools.is_prime(q_value):
        raise ValueError(f"Q({q_value}) is not prime")
    if (p_value - 1) % q_value != 0:
        raise ValueError(
            f"P - 1 isn't devisable by Q {p_value - 1} % {q_value} != 0"
        )


def dsa_sign(data, p_value, q_value, x_value, k_value, g_value):
    if len(data.split(":")) != 1:
        raise ValueError("I just need H(m)")
    data = int(data)

    r_value = (pow(g_value, k_value) % p_value) % q_value
    if r_value == 0:
        raise ValueError("Incorrect k: r equals 0")

    s_value = (crypto_tools.inverse_modulo_numb(k_value, q_value) *
               ((data + x_value * r_value) % q_value))

    if s_value == 0:
        raise ValueError("Incorrect k: s equals 0")

    return f"{data}:{int(r_value)}:{int(s_value)}"


def dsa_verify(data, p_value, q_value, g_value, open_key):
    if len(data.split(":")) != 3:
        raise ValueError("I need H(m):r:s")
    r_value = int(data.split(":")[1])
    s_value = int(data.split(":")[2])
    data = int(data.split(":")[0])

    w_value = crypto_tools.inverse_modulo_numb(s_value, q_value)
    u1_value = (data * w_value) % q_value
    u2_value = (r_value * w_value) % q_value
    v_value = (
        (pow(g_value, u1_value) * pow(open_key, u2_value) % p_value) % q_value
    )
    return "Verified" if v_value == r_value else "Error"


def dsa_processing(data, p_value, q_value, x_value, k_value, encrypt):
    check_params(p_value, q_value)

    h_value = 2
    g_value = pow(h_value, int((p_value - 1) / q_value))
    while g_value == 1:
        h_value += 1
        if h_value == p_value - 1:
            raise ValueError(
                f"Cannot find correct h_value in range(1;{p_value - 1})"
            )
        g_value = pow(h_value, int((p_value - 1) / q_value))
    open_key = pow(h_value, x_value) % q_value

    if encrypt == "sign":
        return dsa_sign(data, p_value, q_value, x_value, k_value, g_value)
    else:
        return dsa_verify(data, p_value, q_value, g_value, open_key)


@crypto_tools.file_manipulation
def dsa(data):
    data = crypto_tools.utf_decoder(data)

    p_value = int(crypto_tools.cterm('input',
                                     'Enter first(p) number: ', 'ans'))
    q_value = int(crypto_tools.cterm('input',
                                     'Enter second(q) number: ', 'ans'))
    x_value = int(crypto_tools.cterm('input',
                                     'Enter secret key(x) number: ', 'ans'))
    k_value = int(crypto_tools.cterm('input',
                                     'Enter secret key(k) number: ', 'ans'))

    encrypt = crypto_tools.cterm('input',
                                 'You want sign or verify: ', 'ans')

    if encrypt != "sign" and encrypt != "verify":
        raise ValueError(f"Incorrect action {encrypt}")

    return dsa_processing(data, p_value, q_value, x_value, k_value, encrypt)


dsa.little_doc = dsa_little_doc
dsa.full_doc = dsa_full_doc
