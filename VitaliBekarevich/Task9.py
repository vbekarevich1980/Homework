# Task 4.9
# Implement a bunch of functions which receive a changeable number of strings and return next parameters:

# 1) characters that appear in all strings

# 2) characters that appear in at least one string

# 3) characters that appear at least in two strings

# 4) characters of alphabet, that were not used in any string

# Note: use `string.ascii_lowercase` for list of alphabet letters

# ```python
# test_strings = ["hello", "world", "python", ]
# print(test_1_1(*strings))
# >>> {'o'}
# print(test_1_2(*strings))
# >>> {'d', 'e', 'h', 'l', 'n', 'o', 'p', 'r', 't', 'w', 'y'}
# print(test_1_3(*strings))
# >>> {'h', 'l', 'o'}
# print(test_1_4(*strings))
# >>> {'a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'm', 'q', 's', 'u', 'v', 'x', 'z'}
# ```

from string import ascii_lowercase


def test_1_1(*strings: str) -> set:

    res = set(strings[0])

    for i in range(1, len(strings)):
        res &= set(strings[i])

    return res


def test_1_2(*strings: str) -> set:

    res = set()

    for string in strings:
        res.update(set(string))

    return res


def test_1_3(*strings: str) -> set:

    res = set()

    for i in range(len(strings)):

        temp_strings = list(strings)
        temp_set = set(temp_strings.pop(i))

        for string in temp_strings:
            res.update(temp_set.intersection(set(string)))

    return res


def test_1_4(*strings: str) -> set:

    res = set(ascii_lowercase)

    for string in strings:
        res.difference_update(set(string))

    return res


print(test_1_1("hello", "world", "python"))
print(test_1_2("hello", "world", "python"))
print(test_1_3("hello", "world", "python"))
print(test_1_4("hello", "world", "python"))
