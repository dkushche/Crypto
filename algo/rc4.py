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
    rc4_prga.x = (rc4_prga.x + 1) % 256
    rc4_prga.y = (rc4_prga.y + scheduled_key[rc4_prga.x]) % 256

    scheduled_buffer = scheduled_key[rc4_prga.x]
    scheduled_key[rc4_prga.x] = scheduled_key[rc4_prga.y]
    scheduled_key[rc4_prga.y] = scheduled_buffer
    r_index = (scheduled_key[rc4_prga.x] + scheduled_key[rc4_prga.y]) % 256
    return scheduled_key[r_index]


def rc4_ksa(byte_key):
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + byte_key[i % len(byte_key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def rc4(data, key, encrypt):
    data, byte_key = rc4_proccess_input(data, key, encrypt)
    cyphered_bytes = bytearray()
    scheduled_key = rc4_ksa(byte_key)
    rc4_prga.x = 0
    rc4_prga.y = 0

    for byte in data:
        cyphered_bytes.append(byte ^ rc4_prga(scheduled_key))
    if encrypt == "encrypt":
        result_str = cyphered_bytes
    else:
        result_str = cyphered_bytes.decode("utf-8")
    return result_str
