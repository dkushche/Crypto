import algo
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
    laters = {
        k: v for k, v in sorted(items, key=lambda item: item[1], reverse=True)
    }
    return laters


def check_char(chars, lang_chars, lang):
    crypto_tools.create_plot({
        "encrypted_text": chars,
        f"{lang}": lang_chars
    })


def freq_analys_processing(data, lang):
    data = crypto_tools.utf_decoder(data)
    laters = form_frequency_dict(data)
    langs = crypto_tools.download_json("algo_storage/freqchars.json")

    if lang == "no":
        for lang in langs:
            check_char(laters, langs[lang], lang)
    else:
        check_char(laters, langs[lang], lang)
    return laters


@crypto_tools.file_manipulation
def freq_analys(data):
    lang = crypto_tools.cterm('input', 'Data language($lang/no): ', 'ans')
    return freq_analys_processing(data, lang)


freq_analys.little_doc = freq_analys_little_doc
freq_analys.full_doc = freq_analys_full_doc
