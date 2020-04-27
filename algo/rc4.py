import crypto_tools


def rc4_proccess_input(data, key, encrypt):
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")
    byte_key = bytearray(key, "utf-8")
    if len(byte_key) > 256:
        raise ValueError("Key len must be <= 256")
    if data.__class__ == str:
        data = bytearray(data, "utf-8")
    return data, byte_key


def rc4_prga(scheduled_key):
    x = 0
    y = 0

    x = (x + 1) % 256
    y = (y + scheduled_key[x]) % 256

    scheduled_key[x], scheduled_key[y] = scheduled_key[y], scheduled_key[x]
    return scheduled_key[(scheduled_key[x] + scheduled_key[y]) % 256]


def rc4_ksa(byte_key):
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + byte_key[i % len(byte_key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def rc4(data, key, encrypt):
    data, byte_key = rc4_proccess_input(data, key, encrypt)
    scheduled_key = rc4_ksa(byte_key)
    cyphered_bytes = bytearray()

    for byte in data:
        cyphered_bytes.append(byte ^ rc4_prga(scheduled_key))
    if encrypt == "encrypt":
        result_str = cyphered_bytes
    else:
        result_str = cyphered_bytes.decode("utf-8")
    return result_str
