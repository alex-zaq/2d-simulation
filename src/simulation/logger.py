import functools
import sys
import time

from loguru import logger

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])


def get_logger():
    return logger


def measure_time(logger=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            execution_time = (end_time - start_time) * 1000  # в миллисекундах

            if logger:
                logger.info(
                    f"Function '{func.__name__}' executed in {execution_time:.2f} ms"
                )
            else:
                print(f"Function '{func.__name__}' executed in {execution_time:.2f} ms")

            return result

        return wrapper

    return decorator
