import crypto_tools
from math import sqrt, ceil


def hill_little_doc():
    return "encrypt/decrypt using hill algo"


def hill_full_doc():
    return """
    Hill algorithm.
    Uses some matrix stuff, check wikipedia plz.
    """


def gen_key_mtx(key, hill_dict, size):
    res_mtx = [[0 for i in range(size)] for j in range(size)]
    inx = 0
    while inx < size ** 2:
        if inx < len(key):
            try:
                res_mtx[inx // size][inx % size] = hill_dict.index(key[inx])
            except ValueError:
                err_msg = f"There is no {key[inx]} in alphabet"
                raise ValueError(err_msg)
        else:
            p_inx = inx - 1
            prev = res_mtx[p_inx // size][p_inx % size]
            res_mtx[inx // size][inx % size] = (prev + 1) % len(hill_dict)
        inx += 1
    return res_mtx


def gen_data_mtx(data, hill_dict, size):
    space_num = hill_dict.index(" ")
    width = ceil(len(data) / size)
    res_mtx = [[space_num for i in range(width)] for j in range(size)]
    inx = 0
    while inx < len(data):
        try:
            res_mtx[inx // width][inx % width] = hill_dict.index(data[inx])
        except ValueError:
            raise ValueError(f"There is no {data[inx]} in alphabet")
        inx += 1
    return res_mtx


def mtx_to_str(mtx, hill_dict):
    res = ""
    for line in mtx:
        for element in line:
            res += hill_dict[int(element) % len(hill_dict)]
    return res


def hill_processing(data, key, encrypt, hill_dict):
    data = crypto_tools.utf_decoder(data)
    mtx_side_size = ceil(sqrt(len(key)))
    key_mtx = gen_key_mtx(key, hill_dict, mtx_side_size)
    if encrypt == "decrypt":
        key_mtx = crypto_tools.inverse_mtx(key_mtx, True, len(hill_dict))
    data_mtx = gen_data_mtx(data, hill_dict, mtx_side_size)
    res_mtx = crypto_tools.mtx_mult(key_mtx, data_mtx)
    result = mtx_to_str(res_mtx, hill_dict)
    return result


@crypto_tools.file_manipulation
def hill(data):
    lang = crypto_tools.cterm('input', 'Data language: ', 'ans')
    key = crypto_tools.cterm('input', 'Enter key: ', 'ans')
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if len(key) < 2:
        raise ValueError("Key must be bigger then 1 char")
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError("Incorrect action")
    hill_dict = crypto_tools.get_param_json_data("alphabets.json", lang)
    return hill_processing(data, key, encrypt, hill_dict)


hill.little_doc = hill_little_doc
hill.full_doc = hill_full_doc
