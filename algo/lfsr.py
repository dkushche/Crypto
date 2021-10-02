from bitarray import bitarray
from math import ceil
import crypto_tools
import json


def lfsr_little_doc():
    return "linear feedback shift register"


def lfsr_full_doc():
    return """
    register size:
        size of linear feedback shift register in bytes
    executive polynomial examples:
        [11, 2, 0]
    start register examples:
        [0, 3]
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


def lfsr_cypher(data, tick, register_size):
    crypto_tools.supl_to_mult(data, register_size)
    result = bytearray()

    for byte in data:
        random_number = next(tick)
        random_number = int.from_bytes(random_number, byteorder='big', signed=False)

        result.append(byte ^ random_number)

    return result


def lfsr_generator(tick, output_size):
    result = bytearray()

    for i in range(output_size):
        result += next(tick)

    return result


def lfsr_processing(data, register_size, exec_xor_pos, start_state, output_size=None):
    if register_size * 8 < max(exec_xor_pos) or register_size * 8 < max(start_state):
        raise ValueError(f"{register_size} smaller then significant bit position {max(max(exec_xor_pos), max(start_state))}")

    tick = lfsr_tick()

    next(tick)
    tick.send(register_size)
    tick.send(start_state)
    tick.send(exec_xor_pos)

    if output_size is None:
        return lfsr_cypher(data, tick, register_size)
    else:
        return lfsr_generator(tick, output_size)


@crypto_tools.file_manipulation()
def lfsr(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    register_size = int(crypto_tools.cterm('input', 'Enter register_size(uint): ', 'ans'))
    if register_size <= 0:
        raise ValueError("Register size must be bigger then 0")

    start_state = json.loads(crypto_tools.cterm('input', 'Enter register start state(list): ', 'ans'))
    if start_state.__class__ != list:
        raise ValueError(f"Incorrect exec_xor_pos class {start_state.__class__}")

    exec_xor_pos = json.loads(crypto_tools.cterm('input', 'Enter executive polynomial xor bits(list): ', 'ans'))
    if exec_xor_pos.__class__ != list:
        raise ValueError(f"Incorrect exec_xor_pos class {exec_xor_pos.__class__}")

    mode = crypto_tools.cterm('input', 'Enter mode(cypher|generator): ', 'ans')

    output_size = None
    if mode in ["cypher", "generator"]:
        if mode == "generator":
            output_size = int(crypto_tools.cterm('input', 'Enter output size: ', 'ans'))
            if output_size <= 0:
                raise ValueError(f"Incorrect output buffer size {output_size}")
    else:
        raise ValueError(f"Incorrect mode {mode}")

    return lfsr_processing(data, register_size, exec_xor_pos, start_state, output_size)



lfsr.little_doc = lfsr_little_doc
lfsr.full_doc = lfsr_full_doc
lfsr.tick = lfsr_tick
