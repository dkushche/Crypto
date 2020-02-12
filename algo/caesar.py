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


def hack_caesar(data):
    key = 0
    found = False
    result = ""
    templates = []
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    try:
        with open("hack_storage/caesar.table", 'r') as table:
            for line in table:
                templates.append(line[:-1])
    except FileNotFoundError:
        print("There is no solving table")
        raise
    while(not found and key < 10000):
        key += 1
        result = caesar(data, key, "decrypt")
        for template in templates:
            if template in result:
                found = True
    if key == 10000:
        return "No answer"
    return '{ "Result string": "' + result + '", "Key":' + str(key) + ' }'
