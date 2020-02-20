from json import load as get_json
"""
    In this file we have functions that
    can read words tables, frequency characteristics
    for any language in hack_storage
    and compare your guessed encrypted words with
    this real words
"""


def read_hack_json(fname):
    try:
        path = "hack_storage/" + fname
        with open(path, "r") as jsn:
            return get_json(jsn)
    except FileNotFoundError:
        print("There is no {0}".format(path))
        raise


def read_lang_table(lang):
    templates = []

    try:
        path = "hack_storage/" + lang + "_words.table"
        with open(path, 'r') as table:
            for line in table:
                templates.append(line[:-1])
        return templates
    except FileNotFoundError:
        print("Can't find " + lang + " table")
        raise


def is_string_reproduced(templates, result):
    """
        Check does any word from dictionary
        in resulting string
    """
    for template in templates:
        if template in result:
            return True
    return False
