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
        zeroes += bin(val).count("0")
        ones += bin(val).count("1")
    whole = zeroes + ones
    perc = ones / whole
    if (perc < 0.6 and perc > 0.4):
        return True
    return False


def generate(data):
    animation = "|/-\\"
    frame = 0
    parameters = []
    coefficient = 2
    while True:
        constant = 0
        while(constant < 1000):
            start_value = 0
            while(start_value < 1000):
                sequence = calc(data['size'], constant, coefficient, start_value)
                if (len(sequence) > 0.7 * data['size'] and check_bits(sequence)):
                    record = {"m": data['size'], "c": constant, "a": coefficient, "f": start_value}
                    parameters.append(record)
                    if len(parameters) > data['amount']:
                        return parameters
                frame = (frame + 1) % len(animation)
                print("\rLoading [" + animation[frame] + "]", end="")
                start_value += 1
            constant += 1
        coefficient += 1


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
                data[i]["sequence"] = calc(data[i]['m'], data[i]['c'], data[i]['a'], data[i]['f'])
        elif action == "generate":
            data = generate(data)
        else:
            raise ValueError("Incorrect action")
    except KeyError:
        raise ValueError("Incorrect input")
    except TypeError:
        raise ValueError("Incorrect input")
    return dumps(data)
