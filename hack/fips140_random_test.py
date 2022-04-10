""" FIPS 140

Random squences generators tester

Parameters
----------
TODO

Returns
-------
TODO

"""

import sys
import crypto_tools


def fips140_random_test_little_doc():
    return "fips140 random algortihms tester"


def fips140_random_test_full_doc():
    return """
    fips140_random_test contains 4 tests:
        * Monobit test
        * Poker test
        * Test amount of series(Runs)
        * Test series lengths(Conditional)
    """


def fips140_random_test_all(data):
    report = ""
    report += fips140_random_test_monobit(data) + "\n"
    report += fips140_random_test_poker(data) + "\n"
    report += fips140_random_test_runs(data) + "\n"
    report += fips140_random_test_conditional(data) + "\n"

    return report


def fips140_random_test_monobit(data):
    if len(data) < 20000:
        raise ValueError("Data length must be >= 20000")

    data = data[:20000]

    ones = data.count('1')
    zeroes = data.count('0')

    status = None
    if not 9654 < ones < 10346 or 9654 < zeroes < 10346:
        status = "success"
    else:
        status = "failure"

    return f"Test monobit {status}: ones({ones}); zeroes({zeroes});"


def fips140_random_test_poker(data):
    if len(data) < 20000:
        raise ValueError("Data length must be >= 20000")

    data = data[:20000]

    blocks = {}
    for i in range(0, 20000, 4):
        if blocks.get(str(data[i: i + 4])[10:-2]):
            blocks[str(data[i: i + 4])[10:-2]] += 1
        else:
            blocks[str(data[i: i + 4])[10:-2]] = 1

    sq_sum = 0
    for i in blocks.values():
        sq_sum += i ** 2

    X = (16 / 5000) * sq_sum - 5000

    status = None
    if 1.03 < X < 57.4:
        status = "success"
    else:
        status = "failure"

    return f"Test poker {status}: X({X})"


def fips140_random_test_runs(data):
    if len(data) < 20000:
        raise ValueError("Data length must be >= 20000")

    data = data[:20000]

    series = {}

    prev_bit = None
    cur_series = 1
    for bit in data:
        if bit == prev_bit:
            cur_series += 1
        else:
            cur_series = min(cur_series, 6)

            if series.get(f"{cur_series}"):
                series[f"{cur_series}"] += 1
            else:
                series[f"{cur_series}"] = 1

            cur_series = 1

        prev_bit = bit

    ranges = {
        "1": (2267, 2733), "2": (1079, 1421), "3": (502, 748),
        "4": (223, 402), "5": (90, 223), "6": (90, 223)
    }

    report = "Test runs:\n"

    for length, amount in ranges.items():
        status = None
        val = None

        if not series.get(f"{length}"):
            status = "failure"
        else:
            val = series[f"{length}"]

            if amount[0] < val < amount[1]:
                status = "success"
            else:
                status = "failure"

        report += f"\tstatus: {status}; {length}: {val}\n"

    return report


def fips140_random_test_conditional(data):
    if len(data) < 20000:
        raise ValueError("Data length must be >= 20000")

    data = data[:20000]

    prev_val = None
    max_series = 0
    cur_series = 1
    for bit in data:
        if prev_val == bit:
            cur_series += 1
        else:
            if cur_series > max_series:
                max_series = cur_series
            cur_series = 1

        prev_val = bit

    status = None
    if max_series > 34:
        status = "failure"
    else:
        status = "success"

    return f"Test conditional {status}: max series = {max_series}"


@crypto_tools.file_manipulation()
def fips140_random_test(data):
    if data.__class__ == str:
        data = bytearray(data, "utf-8")

    method = crypto_tools.cterm(
        'input',
        'Enter fips140 method(monobit|poker|runs|conditional|all): ',
        'ans'
    )

    try:
        fips140_test = getattr(sys.modules[__name__], "fips140_random_test_" + method)

        data_in_bits = crypto_tools.to_bitarray(data)

        crypto_tools.cterm("output", f"Sequence : {data_in_bits}", "inf")

        return fips140_test(data_in_bits)
    except AttributeError as err:
        raise ValueError(f"No such method: {method}") from err


fips140_random_test.little_doc = fips140_random_test_little_doc
fips140_random_test.full_doc = fips140_random_test_full_doc
