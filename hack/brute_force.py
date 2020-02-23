import algo
from lang_tools import *

def crush_caesar(data, lang):
    key = 1
    result = ""
    templates = get_param_json_data("words.json", lang)
    caesar_dictionary = get_param_json_data("alphabets.json", lang)

    while(key != len(caesar_dictionary)):
        result = algo.caesar(data, lang, key, "decrypt")
        if (is_string_reproduced(templates, result)):
            break
        key += 1
    if key == len(caesar_dictionary):
        return "None"
    return '{{ "Result string": "{0}", "Key":{1} }}'.format(result, key)


def brute_force(data, algo, lang):
    algoes = { "caesar": crush_caesar }

    if algo not in algoes:
        raise ValueError("Incorrect algo")
    if lang == "no":
        langs = read_algo_json("alphabets.json")
        for lang in langs:
            result = algoes[algo](data, lang)
            if not result == "None":
                return "Language: {0}\n{1}".format(lang, result)
    else:
        return algoes[algo](data, lang)