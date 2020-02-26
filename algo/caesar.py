import crypto_tools


def caesar(data, lang, key, encrypt):
    if encrypt == "decrypt":
        key = key * -1
    elif encrypt != "encrypt":
        raise ValueError("Incorrect type")
    caesar_dict = crypto_tools.get_param_json_data("alphabets.json", lang)

    result = ""
    data = crypto_tools.utf_decoder(data)
    for char in data:
        try:
            index = caesar_dict.index(char)
        except ValueError:
            err_str = "There is no " + char + " character in alphabet"
            raise ValueError(err_str)
        index = (index + key) % len(caesar_dict)
        result = result + caesar_dict[index]
    return result
