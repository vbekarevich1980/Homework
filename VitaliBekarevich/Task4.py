# Task 7.4
# Implement decorator for suppressing exceptions. If exception does not occur write log to console.
import logging
from contextlib import suppress

logging.basicConfig(level=logging.INFO)


def zero_division_suppression(division_function):

    def wrapper(*args, **kwargs):
        with suppress(ZeroDivisionError):
            result = division_function(*args, **kwargs)
            logging.info('No exceptions have occurred.')
            return result
    return wrapper


@zero_division_suppression
def my_div(number, divider):
    print(f'I am trying to dived {number} by {divider} ...')
    return number / divider


print(my_div(10, 2))
print(my_div(10, 0))
