import time
import functools
from crypto_tools import cterm


def check_time(function):
    @functools.wraps(function)
    def wrapper_check_time(*args, **kwargs):
        start_time = time.process_time()
        result = function(*args, **kwargs)
        end_time = time.process_time()
        dtime = str(end_time - start_time)
        cterm("output", function.__name__ +
              " spent " + dtime + " seconds", "inf")
        return result
    return wrapper_check_time
