""" Frequency analysis

Encrypted text analyzer. Helps to compare
frequency characteristics of encrypted and clear textes and
connect symbols

Parameters
----------
TODO

Returns
-------
TODO

"""

import crypto_tools


def freq_analys_little_doc():
    return "find frequency characteristic of text"


def freq_analys_full_doc():
    return """
    Help you compare frequency characteristics of text
    """


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
    return dict(sorted(items, key=lambda item: item[1], reverse=True))


def check_char(chars, lang_chars, lang):
    crypto_tools.create_plot({
        "encrypted_text": chars,
        f"{lang}": lang_chars
    })


def freq_analys_processing(data, lang):
    data = crypto_tools.utf_decoder(data)
    laters = form_frequency_dict(data)
    langs = crypto_tools.download_json("crypto_storage/freqchars.json")

    if lang == "no":
        for cur_lang in langs:
            check_char(laters, langs[cur_lang], cur_lang)
    else:
        check_char(laters, langs[lang], lang)
    return laters


@crypto_tools.file_manipulation()
def freq_analys(data):
    lang = crypto_tools.cterm('input', 'Data language($lang/no): ', 'ans')
    return freq_analys_processing(data, lang)


freq_analys.little_doc = freq_analys_little_doc
freq_analys.full_doc = freq_analys_full_doc
