# Task 4.5
# Implement a function `get_digits(num: int) -> Tuple[int]` which returns a tuple
# of a given integer's digits.
# Example:
# ```python
# >>> split_by_index(87178291199)
# (8, 7, 1, 7, 8, 2, 9, 1, 1, 9, 9)
# ```

def get_digits(num: int) -> tuple:

    return tuple((int(digit) for digit in str(num)))


user_num = int(input('Input your string:\n% '))
print(get_digits(user_num))
