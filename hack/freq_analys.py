import algo
from .lang_tools import *
from .create_plot import *


def form_frequency_dict(data):
    """
        Profile
        Forms sorted dictionary with
        probabilities values for every character
    """
    laters = {}

    for char in data:
        if char in laters:
            laters[char] += 1
        else:
            laters.update({char: 1})
    for later in laters:
        laters[later] = laters[later] / len(data) * 100
    items = laters.items()
    laters = {
        k: v for k, v in sorted(items, key=lambda item: item[1], reverse=True)
    }
    return laters


def check_char(chars, lang_chars, lang):
    exec('create_plot(encrypted_text=chars, {0}=lang_chars)'.format(lang))


def freq_analys(data, lang):
    data = algo.utf_decoder(data)
    laters = form_frequency_dict(data)
    langs = read_algo_json("freqchars.json")

    if lang == "no":
        for lang in langs:
            check_char(laters, langs[lang], lang)
    else:
        check_char(laters, langs[lang], lang)
    return laters
