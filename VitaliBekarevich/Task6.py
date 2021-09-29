# Task 5.6
# Implement a decorator `call_once` which runs a function or method once and caches the result.
# All consecutive calls to this function should return cached result no matter the arguments.

# ```python
# @call_once
# def sum_of_numbers(a, b):
#     return a + b
#
# print(sum_of_numbers(13, 42))
# >>> 55
# print(sum_of_numbers(999, 100))
# >>> 55
# print(sum_of_numbers(134, 412))
# >>> 55
# print(sum_of_numbers(856, 232))
# >>> 55
# ```

def call_once(function_to_decorate):

    cache = None

    def wrapper(*args, **kwargs):
        nonlocal cache
        if cache is None:
            cache = function_to_decorate(*args, **kwargs)
        return cache
    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


# print(call_once(sum_of_numbers)(999, 100))
print(sum_of_numbers(13, 42))
print(sum_of_numbers(999, 100))
print(sum_of_numbers(134, 412))
print(sum_of_numbers(856, 232))
