import time
import signal
from contextlib import contextmanager

def timing_measure(func):
    '''Decorator to measure the execution time of a function.'''
    def wrapper(*args):
        timeStart = time.time()
        ret = func(*args)
        timeEnd = time.time()
        runtime = timeEnd - timeStart

        return ret, runtime
    return wrapper

@timing_measure
def measure_algorithm_runtime(algorithm, *args):
    return algorithm(*args)

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds: int):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
