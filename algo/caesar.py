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
    print(data)
    print("Not ready")
    return "Aue"
