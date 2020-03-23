from json import load as get_json

"""
    In this file we have functions that
    can read words tables, frequency characteristics
    for any language in algo_storage
    and compare your guessed encrypted words with
    this real words
"""


def utf_decoder(data):
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    return data


def is_string_reproduced(templates, result):
    """
        Check does any word from dictionary
        in resulting string
    """
    for template in templates:
        if template in result:
            return True
    return False
