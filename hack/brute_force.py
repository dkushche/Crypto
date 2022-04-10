""" Brute force

Caesar broot forcing

Parameters
----------
TODO

Returns
-------
TODO

"""

import algo
import crypto_tools


def brute_force_little_doc():
    return "hack using algorithm brute force"


def brute_force_full_doc():
    return """
    Dear old bruteforce. I wrote only for
    caesar algorithm
    """


def crush_caesar_try(data, lang, caesar_dictionary):
    key = 1
    result = ""
    templates = crypto_tools.get_param_json_data("words.json", lang)

    while key != len(caesar_dictionary):
        result = algo.caesar.processor(data, lang, -1 * key)
        if crypto_tools.is_string_reproduced(templates, result):
            break
        key += 1
    if key == len(caesar_dictionary):
        return "None"
    return f'{{ "Result string": "{result}", "Key":{key} }}'


def crush_caesar(data):
    sentence = "Do you know language($lang/no): "
    lang = crypto_tools.cterm("input", sentence, "ans")

    langs = crypto_tools.download_json("crypto_storage/alphabets.json")
    if lang == "no":
        for lang in langs:
            result = crush_caesar_try(data, lang, langs[lang])
            if result != "None":
                return f"Language: {lang}\n{result}"
        return "None"
    return crush_caesar_try(data, lang, langs[lang])


@crypto_tools.check_time
def brute_force_processing(data, algorithm):
    algoes = {
        "caesar": crush_caesar
    }

    if algorithm not in algoes:
        raise ValueError("Incorrect algo")
    return algoes[algorithm](data)


@crypto_tools.file_manipulation()
def brute_force(data):
    algorithm = crypto_tools.cterm('input',
                              'What algo was used: ', 'ans')
    return brute_force_processing(data, algorithm)


brute_force.little_doc = brute_force_little_doc
brute_force.full_doc = brute_force_full_doc
