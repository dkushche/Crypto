import algo
from .hack_decorators import check_time
from lang_tools import *


def crush_xor(data):
    print("I want to do this, but later")
    pass


def crush_caesar_try(data, lang, caesar_dictionary):
    key = 1
    result = ""
    templates = get_param_json_data("words.json", lang)

    while(key != len(caesar_dictionary)):
        result = algo.caesar(data, lang, key, "decrypt")
        if (is_string_reproduced(templates, result)):
            break
        key += 1
    if key == len(caesar_dictionary):
        return "None"
    return '{{ "Result string": "{0}", "Key":{1} }}'.format(result, key)


def crush_caesar(data):
    lang = input('?>> Do you know language($lang/no): ')

    if lang == "no":
        langs = read_algo_json("alphabets.json")
        for lang in langs:
            result = crush_caesar_try(data, lang, langs[lang])
            if not result == "None":
                return "Language: {0}\n{1}".format(lang, result)
        return "None"
    else:
        return crush_caesar_try(data, lang)


@check_time
def brute_force(data, algo):
    algoes = { 
        "caesar": crush_caesar,
        "xor" : crush_xor
    }

    if algo not in algoes:
        raise ValueError("Incorrect algo")
    return algoes[algo](data)
