import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'execution time for {func.__name__!r} = {(end - start):.4f} secs.')
        return result

    return wrapper
