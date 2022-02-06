""" Caesar algorithm

The simple and easy method of encryption technique.
It is simple type of substitution cipher. Each letter of plain text
is replaced by a letter with some fixed number of positions down with alphabet.

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools


def caesar_little_doc():
    return "encrypt/decrypt using caesar algo"


def caesar_full_doc():
    return """
    Just caesar algorithm.
    Uses dictionary from alphabers.json and move characters
    left and right
    """


def caesar_processing(data, lang, key):
    caesar_dict = crypto_tools.get_param_json_data("alphabets.json", lang)

    result = ""
    data = crypto_tools.utf_decoder(data)
    for char in data:
        try:
            index = caesar_dict.index(char)
        except ValueError as err:
            err_str = "There is no " + char + " character in alphabet"
            raise ValueError(err_str) from err
        index = (index + key) % len(caesar_dict)
        result = result + caesar_dict[index]
    return result


@crypto_tools.file_manipulation()
def caesar(data):
    lang = crypto_tools.cterm('input', 'Data language: ', 'ans')
    key = int(crypto_tools.cterm('input', 'Enter key(int): ', 'ans'))
    encrypt = crypto_tools.cterm('input',
                                 'You want encrypt or decrypt: ', 'ans')

    if encrypt == "decrypt":
        key = key * -1
    elif encrypt != "encrypt":
        raise ValueError("Incorrect type")
    return caesar_processing(data, lang, key)


caesar.little_doc = caesar_little_doc
caesar.full_doc = caesar_full_doc
caesar.processor = caesar_processing
