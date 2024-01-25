from typing import Tuple
from functools import wraps
import time
import logging


def retry_on_except(exceptions: Tuple, max_attempts: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 1
            while attempts <= max_attempts:
                try:
                    res = func(*args, *kwargs)
                    return res
                except exceptions as e:
                    if attempts == max_attempts:
                        logging.error(
                            f"Exception {e} occurred after {attempts} attempts"
                        )
                        raise e
                    else:
                        logging.error(f"Attempt {attempts} failed")
                        time.sleep(1)
                    attempts += 1

        return wrapper

    return decorator
