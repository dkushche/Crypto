import time
import matplotlib.pylab as plt
from json import load as get_json


dictionary = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ _.0123456789"


def caesar(data, key, encrypt):
    if encrypt == "decrypt":
        key = key * -1
    elif encrypt != "encrypt":
        print("Incorrect type")
        raise ValueError
    result = ""
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    for char in data:
        try:
            index = dictionary.index(char)
        except ValueError:
            print("There is no " + char + " character in dictionary")
            raise
        index = (index + key) % len(dictionary)
        result = result + dictionary[index]
    return result

def read_caesar_table():
    templates = []

    try:
        with open("hack_storage/caesar.table", 'r') as table:
            for line in table:
                templates.append(line[:-1])
        return templates
    except FileNotFoundError:
        print("There is no solving table")
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

def brute_force(data):
    key = 0
    found = False
    result = ""
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    templates = read_caesar_table()
    while(not found and key < 10000):
        key += 1
        result = caesar(data, key, "decrypt")
        for template in templates:
            if template in result:
                found = True
    if key == 10000:
        return "No answer"
    return '{ "Result string": "' + result + '", "Key":' + str(key) + ' }'

def create_subplot(start_data, name, id):
    lists = start_data.items()
    x, y = zip(*lists)
    plt.subplot(2, 1, id)
    plt.xlabel(name)
    plt.plot(x, y)

def frequency_characteristic(data):
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    normal_text = read_frequency_characteristic()
    laters = {}
    for char in data:
        if char == ' ':
            char = 'S'
        if char in laters:
            laters[char] += 1
        else:
            laters.update({char: 1})
    for later in laters:
        laters[later] = laters[later] / len(data) * 100
    create_subplot(laters, "ciphered data", 1)
    create_sub-plot(normal_text, "russian text", 2)
    #Here we need to sort reverse our arrays and check characters
    plt.show()

def hack_caesar(data):
    try:
        one_time = time.clock()
        brute_result = brute_force(data)
        two_time = time.clock()
        print("Brute force needs " + str(two_time - one_time) + " seconds to solve")
        freq_char_result = frequency_characteristic(data)
        one_time = time.clock()
        print("freq_char needs " + str(abs(one_time - two_time)) + " seconds to solve")
        return brute_result
    except ValueError:
        raise FileNotFoundError
