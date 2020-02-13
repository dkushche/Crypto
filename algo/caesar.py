

caesar_dictionary = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ _.0123456789"


def caesar(data, key, encrypt):
    if encrypt == "decrypt":
        key = key * -1
    elif encrypt != "encrypt":
        raise ValueError("Incorrect type")
    result = ""
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    for char in data:
        try:
            index = caesar_dictionary.index(char)
        except ValueError:
            raise ValueError("There is no " + char + " character in caesar_dictionary")
        index = (index + key) % len(caesar_dictionary)
        result = result + caesar_dictionary[index]
    return result
