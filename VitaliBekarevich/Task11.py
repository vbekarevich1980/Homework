# Task 7.11
# Implement a generator which will generate [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number)
# endlessly.
# Example:
# ```python
# gen = endless_fib_generator()
# while True:
#     print(next(gen))
# >>> 1 1 2 3 5 8 13 ...
# ```
from time import sleep


def endless_fib_generator():
    prev_number = 0
    curr_number = 1
    yield prev_number
    while True:
        yield curr_number
        prev_number, curr_number = curr_number, prev_number + curr_number


if __name__ == '__main__':
    gen = endless_fib_generator()
    while True:
        print(next(gen))
        sleep(1)
