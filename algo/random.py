import crypto_tools
from json import loads
from json import dumps
from json.decoder import JSONDecodeError


"""
    m -> needed set size
    c -> constant that we need to add
    a -> coefficient
    also we need first value for sequence
    we call it f
    main_formula
        x[i] = (a * x[i - 1] + c) % m
"""


def check_bits(sequence):
    zeroes = 0
    ones = 0
    for val in sequence:
        zeroes += "{0:b}".format(val).count("0")
        ones += "{0:b}".format(val).count("1")
    whole = zeroes + ones
    perc = ones / whole
    if (perc > 0.4 and perc < 0.6):
        return True
    return False


def generate(data):
    animation = "|/-\\"
    frame = 0
    parameters = []
    coeff = 2
    while True:
        constant = 0
        while(constant < 1000):
            start_value = 0
            while(start_value < 1000):
                sequence = calc(data['size'], constant, coeff, start_value)
                needed_len = 0.7 * data['size']
                if (len(sequence) > needed_len and check_bits(sequence)):
                    record = {"m": data['size'], "c": constant,
                              "a": coeff, "f": start_value}
                    parameters.append(record)
                    if len(parameters) == data['amount']:
                        print("")
                        return parameters
                frame = (frame + 1) % len(animation)
                print("\rLoading [" + animation[frame] + "] ", end="")
                print("{0}/{1}".format(len(parameters), data['amount']), end="")
                start_value += 1
            constant += 1
        coeff += 1


def calc(size, constant, coefficient, start_value):
    sequence = [start_value]
    while True:
        new_value = (coefficient * sequence[-1] + constant) % size
        if new_value in sequence:
            break
        sequence.append(new_value)
    return sequence


def random(data, action):
    try:
        data = crypto_tools.utf_decoder(data)
        data = loads(data)
    except JSONDecodeError:
        raise ValueError("Incorrect input")
    try:
        if action == "calc":
            for i in range(len(data)):
                data[i]["sequence"] = calc(data[i]['m'], data[i]['c'],
                                           data[i]['a'], data[i]['f'])
                data[i]["bin_sequence"] = []
                for num in data[i]["sequence"]:
                    data[i]["bin_sequence"].append("{0:b}".format(num))
        elif action == "generate":
            data = generate(data)
        else:
            raise ValueError("Incorrect action")
    except KeyError:
        raise ValueError("Incorrect input")
    except TypeError:
        raise ValueError("Incorrect input")
    return dumps(data, sort_keys=True, indent=4)
