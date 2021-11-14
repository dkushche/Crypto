import crypto_tools
from .des import des_processing


def triple_des_little_doc():
    return "triple_des_little_doc"


def triple_des_full_doc():
    return """
    triple_des_full_doc
    """


def triple_des_pre_processing(key):
    if len(key) > 7 * 3:
        raise ValueError(f"Too big key. Max len required: {7 * 3}")
    else:
        crypto_tools.supl_to_mult(key, 7 * 3)


def triple_des_processing(data, key, encrypt):
    triple_des_pre_processing(key)

    sub_keys = [key[i:i + 7] for i in range(0, len(key), 7)]

    cur_encrypt = encrypt

    for i in range(3):
        sub_key = sub_keys[i] if encrypt == "encrypt" else sub_keys[2 - i]

        data = des_processing(data, sub_key, cur_encrypt)

        cur_encrypt = "decrypt" if cur_encrypt == "encrypt" else "encrypt"

    return data


@crypto_tools.file_manipulation()
def triple_des(data):
    if data.__class__ == str:
        data = bytearray(data.encode())

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')
    if encrypt != "decrypt" and encrypt != "encrypt":
        raise ValueError("Incorrect type")

    res_data = triple_des_processing(data, key, encrypt)

    if encrypt == "encrypt":
        result_str = res_data
    else:
        result_str = res_data.decode()

    return result_str


triple_des.little_doc = triple_des_little_doc
triple_des.full_doc = triple_des_full_doc

