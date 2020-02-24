import time
import functools


def check_time(function):
    @functools.wraps(function)
    def wrapper_check_time(*args, **kwargs):
        start_time = time.process_time()
        result = function(*args, **kwargs)
        end_time = time.process_time()
        dtime = str(end_time - start_time)
        print(function.__name__ + " spent " + dtime + " seconds")
        return result
    return wrapper_check_time
