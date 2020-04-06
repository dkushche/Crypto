import algo
import crypto_tools
from .hack_decorators import check_time


def crush_caesar_try(data, lang, caesar_dictionary):
    key = 1
    result = ""
    templates = crypto_tools.get_param_json_data("words.json", lang)

    while(key != len(caesar_dictionary)):
        result = algo.caesar(data, lang, key, "decrypt")
        if (crypto_tools.is_string_reproduced(templates, result)):
            break
        key += 1
    if key == len(caesar_dictionary):
        return "None"
    return '{{ "Result string": "{0}", "Key":{1} }}'.format(result, key)


def crush_caesar(data):
    sentence = "Do you know language($lang/no): "
    lang = crypto_tools.cterm("input", sentence, "ans")

    langs = crypto_tools.download_json("algo_storage/alphabets.json")
    if lang == "no":
        for lang in langs:
            result = crush_caesar_try(data, lang, langs[lang])
            if not result == "None":
                return "Language: {0}\n{1}".format(lang, result)
        return "None"
    else:
        return crush_caesar_try(data, lang, langs[lang])


@check_time
def brute_force(data, algo):
    algoes = {
        "caesar": crush_caesar
    }

    if algo not in algoes:
        raise ValueError("Incorrect algo")
    return algoes[algo](data)
