import time
import crypto_tools
from math import ceil
from .xor import xor_processing
from .triple_des import triple_des_processing


def ansi_x9_17_little_doc():
    return "ansi_x9_17_little_doc"


def ansi_x9_17_full_doc():
    return """
    ansi_x9_17_full_doc
    """


def ansi_x9_17_tick():
    triple_des_key = yield
    v0 = yield

    while True:
        stage_0 = int(time.time() * 1000000).to_bytes(8, byteorder='big')
        stage_1 = triple_des_processing(stage_0, triple_des_key, "encrypt")
        stage_2 = xor_processing(stage_1, v0, "encrypt")
        stage_3 = triple_des_processing(stage_2, triple_des_key, "encrypt")
        stage_4 = xor_processing(stage_1, stage_3, "encrypt")
        stage_5 = triple_des_processing(stage_4, triple_des_key, "encrypt")

        v0 = stage_5
        yield stage_3


def ansi_x9_17_init(triple_des_key, v0):
    tick = ansi_x9_17_tick()

    next(tick)
    tick.send(triple_des_key)
    tick.send(v0)

    return tick


def ansi_x9_17_pre_processing(key, v0):
    if len(key) > 7 * 2:
        raise ValueError(f"Too big key. Max len required: {7 * 2}")
    else:
        crypto_tools.supl_to_mult(key, 7 * 2)

    if len(v0) > 8:
        raise ValueError(f"Too big key. Max len required: {7 * 2}")
    else:
        crypto_tools.supl_to_mult(v0, 8)

    return key + key[:7]


def ansi_x9_17_processing(output_size, key, v0):
    triple_des_key = ansi_x9_17_pre_processing(key, v0)
    result = bytearray()

    tick = ansi_x9_17_init(triple_des_key, v0)

    for i in range(ceil(output_size / 8)):
        result += next(tick)

    return result[:output_size]


@crypto_tools.file_manipulation(read_data=False)
def ansi_x9_17():
    output_size = int(crypto_tools.cterm('input', 'Enter output size(bytes): ', 'ans'))
    if output_size <= 0:
        raise ValueError(f"Incorrect output buffer size {output_size}")

    key = crypto_tools.cterm('input', 'Enter key(str): ', 'ans')
    if key.__class__ == str:
        key = bytearray(key.encode())

    v0 = crypto_tools.cterm('input', 'Enter v0(str): ', 'ans')
    if v0.__class__ == str:
        v0 = bytearray(v0.encode())

    return ansi_x9_17_processing(output_size, key, v0)


ansi_x9_17.little_doc = ansi_x9_17_little_doc
ansi_x9_17.full_doc = ansi_x9_17_full_doc
