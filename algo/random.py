""" Random

Self written random generator

Parameters
----------
    m -> needed set size
    c -> constant that we need to add
    a -> coefficient
    also we need first value for sequence
    we call it f
    main_formula
        x[i] = (a * x[i - 1] + c) % m

Returns
-------
TODO

"""


from json import loads, dumps, JSONDecodeError
from time import sleep
import crypto_tools


def random_little_doc():
    return "find arguments/create random sequences"


def random_full_doc():
    return """
    if you want to calc sequences

    [ {"a": 21, "c": 1, "f": 0, "m": 100} ]
    m -> needed set size
    c -> constant that we need to add
    a -> coefficient
    also we need first value for sequence we call it is f

    The great thing that you may enter any amount of dictionaries with parameters

    if you want to generate this values write
    { "amount": $number_of_parameters_for_sequences, "size": $size_of_sequence(m) }
    """


def bitlen(sequence):
    res = 0
    for val in sequence:
        res += len("{0:b}".format(val))
    return res


def form_anim_pack(have, need):
    control_package = {
        "msg": "Loading [{0}]  {1}/" + str(need),
        "objs_for_anim": [[['|', '/', '-', '\\'], 0]],
        "dynamic_values": [[have, 1]],
        "fps": 1
    }
    return control_package


def check_bits(sequence):
    if bitlen(sequence) != 20000:
        raise ValueError("Incorrect sequence bitlen")
    zeroes = 0
    ones = 0
    for val in sequence:
        zeroes += "{0:b}".format(val).count("0")
        ones += "{0:b}".format(val).count("1")
    return 9000 < ones < 11000


def check_len(sequence, dsize):
    needed_len = 0.7 * dsize
    return len(sequence) > needed_len


def generate(data):
    parameters = []
    anim_ctrl_pack = form_anim_pack(len(parameters), data['amount'])
    anim_id = crypto_tools.create_animation(anim_ctrl_pack)
    coeff = 2
    while True:
        constant = 0
        while constant < 1000:
            start_value = 0
            while start_value < 1000:
                nrp_seq, bit_seq = calc(data['size'], constant,
                                        coeff, start_value, 20000)
                if (check_len(nrp_seq, data['size']) and check_bits(bit_seq)):
                    record = {"m": data['size'], "c": constant,
                              "a": coeff, "f": start_value}
                    parameters.append(record)
                    anim_ctrl_pack["dynamic_values"][0][0] = len(parameters)
                    if len(parameters) == data['amount']:
                        sleep(1)
                        crypto_tools.destroy_animation(anim_id, anim_ctrl_pack)
                        return parameters
                start_value += 1
            constant += 1
        coeff += 1


def replay_check(sequence, new_value):
    for i in range(len(sequence)):
        if new_value == sequence[i] and i != 0 \
           and sequence[-1] == sequence[i - 1]:
            return False
    return True


def calc(modul, constant, coefficient, start_value, bit_len):
    no_replay = True
    no_bits = True
    no_replay_sequence = [start_value]
    by_bits_sequence = [start_value]
    bits = len("{0:b}".format(start_value))

    while no_replay or no_bits:
        start_value = (coefficient * start_value + constant) % modul

        if no_replay:
            no_replay = replay_check(no_replay_sequence, start_value)
            if not no_replay:
                no_replay_sequence.pop()
            else:
                no_replay_sequence.append(start_value)
        if no_bits:
            by_bits_sequence.append(start_value)

        bits += len("{0:b}".format(start_value))
        if bits >= bit_len:
            no_bits = False
            by_bits_sequence[-1] >>= bits - bit_len
    return no_replay_sequence, by_bits_sequence


def random_processing(data, action):
    try:
        data = crypto_tools.utf_decoder(data)
        data = loads(data)
        if action == "calc":
            for i in range(len(data)):
                nrp_seq, bit_seq = calc(data[i]['m'], data[i]['c'],
                                        data[i]['a'], data[i]['f'],
                                        20000)
                data[i]["sequence"] = nrp_seq
                data[i]["bin_sequence"] = ""
                for num in bit_seq:
                    data[i]["bin_sequence"] += "{0:b}".format(num)
        elif action == "generate":
            data = generate(data)
        else:
            raise ValueError("Incorrect action")
    except (KeyError, TypeError, JSONDecodeError) as err:
        raise ValueError("Incorrect input") from err
    return dumps(data, sort_keys=True, indent=4)


@crypto_tools.file_manipulation()
def random(data):
    action = crypto_tools.cterm('input',
                                'You want (calc,generate) sequence(s): ',
                                'ans')
    return random_processing(data, action)


random.little_doc = random_little_doc
random.full_doc = random_full_doc
