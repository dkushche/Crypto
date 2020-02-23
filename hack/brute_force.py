import algo

def crush_caesar(data):
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


def brute_force(algo, data, lang):
    raise ValueError("Brute Force")

if __name__ == "__main__":
    print("Just check")
