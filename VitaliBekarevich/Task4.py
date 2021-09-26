# Task 4.4
# Implement a function `split_by_index(s: str, indexes: List[int]) -> List[str]`
# which splits the `s` string by indexes specified in `indexes`. Wrong indexes
# must be ignored.
# Examples:
# ```python
# >>> split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])
# ["python", "is", "cool", ",", "isn't", "it?"]
#
# >>> split_by_index("no luck", [42])
# ["no luck"]
# ```

def split_by_index(s: str, indexes: list) -> list:

    i = 0
    while indexes[i] <= 0:  # "<" if slice [:0] i.e. [''] is required
        i += 1

    res = [s[:indexes[i]]]

    for j in range(i + 1, len(indexes)):
        if indexes[j] < len(s):  # "<=" if slice [len():] i.e. [''] is required
            res.append(s[indexes[j - 1]:indexes[j]])
        else:
            res.append(s[indexes[j - 1]:])
            break

    return res


user_string = input('Input your string:\n% ')
print(split_by_index(user_string, [-1, -3, 0, 6, 8, 12, 13, 18, 19, 20, 21, 22, 23, 25]))
