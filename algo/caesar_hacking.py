import time
import functools
import matplotlib.pyplot as plt
from json import load as get_json
from algo import caesar, caesar_dictionary, utf_decoder


def read_caesar_table():
    templates = []

    try:
        with open("hack_storage/caesar.table", 'r') as table:
            for line in table:
                templates.append(line[:-1])
        return templates
    except FileNotFoundError:
        print("Can't find caesar solving table")
        raise


def read_frequency_characteristic():
    normal_text = {}

    try:
        with open("hack_storage/caesar_freqchar.json", "r") as jsn:
            normal_text = get_json(jsn)
        return normal_text
    except FileNotFoundError:
        print("There is no frequncy characteristic")
        raise


def create_subplot(start_data, name, id):
    lists = start_data.items()
    x, y = list(zip(*lists))
    plt.subplot(2, 1, id)
    plt.grid(True)
    plt.title(name)
    x = list(x)
    spec_sym = {' ': 'S', '.': 'P', '_': 'U'}
    for i in range(len(x)):
        if x[i] in spec_sym:
            x[i] = spec_sym[x[i]]
    plt.plot(x, y)


def save_plot(laters, normal_text):
    create_subplot(laters, "ciphered data", 1)
    create_subplot(normal_text, "russian text", 2)
    plt.subplots_adjust(hspace=0.5)
    plt.savefig("last_frequency_char.png")


def check_time(function):
    @functools.wraps(function)
    def wrapper_check_time(*args, **kwargs):
        start_time = time.process_time()
        result = function(*args, **kwargs)
        end_time = time.process_time()
        dtime = str(end_time - start_time)
        print(function.__name__ + " spent " + dtime + " seconds")
        return result
    return wrapper_check_time


def is_string_reproduced(templates, result):
    for template in templates:
        if template in result:
            return True
    return False


def form_frequency_dict(data):
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


@check_time
def brute_force(data):
    key = 1
    result = ""
    templates = read_caesar_table()

    while(key != len(caesar_dictionary)):
        result = caesar(data, key, "decrypt")
        if (is_string_reproduced(templates, result)):
            break
        key += 1
    if key == len(caesar_dictionary):
        return "None"
    return '{{ "Result string": "{0}", "Key":{1} }}'.format(result, key)


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


@check_time
def frequency_characteristic(data, verbose):
    normal_text = read_frequency_characteristic()
    templates = read_caesar_table()
    laters = form_frequency_dict(data)
    result, key, tries = freq_comp(laters, normal_text, templates, data)

    if not result:
        return "None"
    if verbose:
        save_plot(laters, normal_text)
    return ('{{ "Result string":"{0}", '
            '"Key":{1}, "Tries":{2} }}').format(result, key, tries)


def hack_caesar(data):
    verbose = input("verbose(true/*): ")
    verbose = True if verbose == "true" else False
    try:
        data = utf_decoder(data)
        brute_result = brute_force(data)
        freq_char_result = frequency_characteristic(data, verbose)
        return """
{{
    "Brute" : {0},
    "FreqChar": {1}
}}""".format(brute_result, freq_char_result)
    except ValueError:
        raise


"""
    Todo:
        Optimization frequency_characteristic
        add verbose for plots
"""
