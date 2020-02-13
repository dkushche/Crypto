import time
import matplotlib.pyplot as plt
from json import load as get_json
from algo import caesar, caesar_dictionary


def read_caesar_table():
    templates = []

    try:
        with open("hack_storage/caesar.table", 'r') as table:
            for line in table:
                templates.append(line[:-1])
        return templates
    except FileNotFoundError:
        print("Can't findb caesar solving table")
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


def is_solved(templates, result):
    for template in templates:
        if template in result:
            return True
    return False


def brute_force(data):
    key = 0
    found = False
    result = ""
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    templates = read_caesar_table()
    while(not found and key < len(caesar_dictionary)):
        key += 1
        result = caesar(data, key, "decrypt")
        if (is_solved(templates, result)):
            break
    if key == len(caesar_dictionary):
        return "No answer"
    return '{ "Result string": "' + result + '", "Key":' + str(key) + ' }'


def create_subplot(start_data, name, id):
    lists = start_data.items()
    x, y = list(zip(*lists))
    plt.subplot(2, 1, id)
    plt.title(name)
    x = list(x)
    spec_sym = {' ': 'S', '.': 'P', '_': 'U'}
    for i in range(len(x)):
        if x[i] in spec_sym:
            x[i] = spec_sym[x[i]]
    plt.plot(x, y)


def frequency_characteristic(data):
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    normal_text = read_frequency_characteristic()
    templates = read_caesar_table()
    laters = {}
    for char in data:
        if char in laters:
            laters[char] += 1
        else:
            laters.update({char: 1})
    for later in laters:
        laters[later] = laters[later] / len(data) * 100
    laters = {k: v for k, v in sorted(laters.items(), key=lambda item: item[1], reverse=True)}
    tries = 0
    for later, lang in zip(laters, normal_text):
        lang_index = caesar_dictionary.index(lang)
        later_index = caesar_dictionary.index(later)
        key = later_index - lang_index
        if key < 0:
            key = len(caesar_dictionary) + key
        result = caesar(data, key, "decrypt")
        tries += 1
        if (is_solved(templates, result)):
            break
    print("Key = " + str(key) + "; tries = " + str(tries))
    create_subplot(laters, "ciphered data", 1)
    create_subplot(normal_text, "russian text", 2)
    plt.subplots_adjust(hspace=0.5)
    plt.savefig("last_frequency_char.png")


def hack_caesar(data):
    try:
        one_time = time.process_time()
        brute_result = brute_force(data)
        two_time = time.process_time()
        print("Brute force needs " + str(two_time - one_time) + " seconds to solve")
        freq_char_result = frequency_characteristic(data)
        one_time = time.process_time()
        print("freq_char needs " + str(abs(one_time - two_time)) + " seconds to solve")
        return brute_result
    except ValueError as err:
        print(err)
        raise FileNotFoundError


"""
    Todo:
        Optimization frequency_characteristic
        Refactoring
        Do something with exceptions
        add verbose for plots
"""