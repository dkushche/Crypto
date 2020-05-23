import crypto_tools
from itertools import cycle

def vigenere_str_to_list(string, vigenere_dict):
    result = list()
    for char in string:
        try:
            result.append(vigenere_dict.index(char))
        except ValueError:
            err_msg = f"There is no {key[inx]} in alphabet"
            raise ValueError(err_msg)
    return result


def vigenere_process_input(data, lang, key, encrypt):
    if encrypt != "encrypt" and encrypt != "decrypt":
        raise ValueError("Incorrect action")
    data = crypto_tools.utf_decoder(data)
    vigenere_dict = crypto_tools.get_param_json_data("alphabets.json", lang)
    num_data = vigenere_str_to_list(data, vigenere_dict)
    num_key = vigenere_str_to_list(key, vigenere_dict)
    return vigenere_dict, num_data, num_key


def vigenere(data, lang, key, encrypt):
    vigenere_dict, num_data, num_key = vigenere_process_input(data, lang, key, encrypt)
    dict_size = len(vigenere_dict)
    num_key = cycle(num_key)
    if (encrypt == "encrypt"):
        num_result = [(a + b) % dict_size for a, b in zip(num_data, num_key)]
    else:
        num_result = [(a + dict_size - b) % dict_size for a, b in zip(num_data, num_key)]
    result_str = ""
    for val in num_result:
        result_str += vigenere_dict[val]
    return result_str
