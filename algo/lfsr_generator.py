import crypto_tools
from bitarray import bitarray
import crypto_tools
import json


def lfsr_generator_little_doc():
    return "linear feedback shift register random generator"


def lfsr_generator_full_doc():
    return """
    register size:
        size of linear feedback shift register in bytes
    executive polynomial examples:
        [11, 2, 0]
    start register examples:
        [0, 3]
    output_size:
        size of sequnce in bytes
    """


def lfsr_tick():
    register_size = yield
    start_state = yield
    exec_xor_pos = yield

    register = bitarray()
    register.frombytes(bytes(register_size))
    for pos in start_state:
        register[pos] = 1

    while True:
        random_number = bitarray()

        for i in range(8):
            updated_bit = 0
            for pos in exec_xor_pos:
                updated_bit ^= register[pos]

            random_number.append(register[0])

            for j in range(register_size * 8 - 1):
                register[j] = register[j + 1]

            register[register_size * 8 - 1] = updated_bit

        yield random_number


def lfsr_init(register_size, exec_xor_pos, start_state):
    if register_size * 8 < max(exec_xor_pos) or register_size * 8 < max(start_state):
        raise ValueError(f"{register_size} smaller then significant bit position {max(max(exec_xor_pos), max(start_state))}")

    tick = lfsr_tick()

    next(tick)
    tick.send(register_size)
    tick.send(start_state)
    tick.send(exec_xor_pos)

    return tick


def lfsr_generator_processing(register_size, exec_xor_pos, start_state, output_size):
    result = bytearray()

    tick = lfsr_init(register_size, exec_xor_pos, start_state)

    for i in range(output_size):
        result += next(tick)

    return result


@crypto_tools.file_manipulation(read_data=False)
def lfsr_generator():
    register_size = int(crypto_tools.cterm('input', 'Enter register_size(uint): ', 'ans'))
    if register_size <= 0:
        raise ValueError("Register size must be bigger then 0")

    start_state = json.loads(crypto_tools.cterm('input', 'Enter register start state(list): ', 'ans'))
    if start_state.__class__ != list:
        raise ValueError(f"Incorrect exec_xor_pos class {start_state.__class__}")

    exec_xor_pos = json.loads(crypto_tools.cterm('input', 'Enter executive polynomial xor bits(list): ', 'ans'))
    if exec_xor_pos.__class__ != list:
        raise ValueError(f"Incorrect exec_xor_pos class {exec_xor_pos.__class__}")

    output_size = int(crypto_tools.cterm('input', 'Enter output size: ', 'ans'))
    if output_size <= 0:
        raise ValueError(f"Incorrect output buffer size {output_size}")

    return lfsr_generator_processing(register_size, exec_xor_pos, start_state, output_size)


lfsr_generator.little_doc = lfsr_generator_little_doc
lfsr_generator.full_doc = lfsr_generator_full_doc
