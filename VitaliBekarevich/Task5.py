# Task 7.5
# Implement function for check that number is even and is greater than 2. Throw different exceptions for this errors.
# Custom exceptions must be derived from custom base exception(not Base Exception class).

class MyException(Exception):
    def __init__(self, error_message):
        self.error_message = error_message


class LessThanTwoError(MyException):
    pass


class NotEvenError(MyException):
    pass


class NotIntegerError(MyException):
    pass


def is_even(number: int) -> bool:

    if not isinstance(number, int):
        raise NotIntegerError('Please, enter an integer number!')
    elif number <= 2:
        raise LessThanTwoError('We agreed to check numbers greater than 2!')
    elif number % 2:
        raise NotEvenError('The number, you entered, is NOT even!')
    else:
        return True


if __name__ == '__main__':
    # print(is_even(-1))
    # print(is_even('2'))
    # print(is_even(3.56))
    print(is_even(4))
