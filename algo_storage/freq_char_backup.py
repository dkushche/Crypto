
def freq_comp(laters, normal_text, templates, data):
    tries = 1
    dispersion = 15
    for later in laters:
        for lang in normal_text:
            if abs(laters[later] - normal_text[lang]) < dispersion:
                result, key = guess_try(lang, later, templates, data)
                if result:
                    return result, key, tries
                tries += 1
            elif laters[later] < normal_text[lang]:
                continue
            else:
                break
    return None, None, None


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
