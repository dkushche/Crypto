from .lfsr_generator import lfsr_init
from bitarray import bitarray
import crypto_tools
import json


def lfsr_little_doc():
    return "cypher using lfsr sequence"


def lfsr_full_doc():
    return """
    register size:
        size of linear feedback shift register in bytes
    executive polynomial examples:
        [11, 2, 0]
    start register examples:
        [0, 3]
    """


def lfsr_processing(data, register_size, exec_xor_pos, start_state):
    tick = lfsr_init(register_size, exec_xor_pos, start_state)

    crypto_tools.supl_to_mult(data, register_size)
    result = bytearray()

    for byte in data:
        random_number = next(tick)
        random_number = int.from_bytes(random_number, byteorder='big', signed=False)

        result.append(byte ^ random_number)

    return result


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

    return lfsr_processing(data, register_size, exec_xor_pos, start_state)


lfsr.little_doc = lfsr_little_doc
lfsr.full_doc = lfsr_full_doc
