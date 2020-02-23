def form_frequency_dict(data):
    """
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


def guess_try(lang, later, templates, data):
    lang_index = caesar_dictionary.index(lang)
    later_index = caesar_dictionary.index(later)
    key = later_index - lang_index
    if key < 0:
        key = len(caesar_dictionary) + key
    result = caesar(data, key, "decrypt")
    if (is_string_reproduced(templates, result)):
        return result, key
    return None, None


def freq_analys(data, lang, algo, verbose):
    raise ValueError("Freq analysis")
