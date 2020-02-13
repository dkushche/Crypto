

caesar_dictionary = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ _.0123456789"


def utf_decoder(data):
    if data.__class__ == bytes or data.__class__ == bytearray:
        data = data.decode("utf-8")
    return data


def caesar(data, key, encrypt):
    if encrypt == "decrypt":
        key = key * -1
    elif encrypt != "encrypt":
        raise ValueError("Incorrect type")
    result = ""
    data = utf_decoder(data)
    for char in data:
        try:
            index = caesar_dictionary.index(char)
        except ValueError:
            err_str = "There is no " + char + " character in caesar_dictionary"
            raise ValueError(err_str)
        index = (index + key) % len(caesar_dictionary)
        result = result + caesar_dictionary[index]
    return result
