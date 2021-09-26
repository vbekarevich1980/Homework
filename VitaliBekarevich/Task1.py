# Task 4.1
# Implement a function which receives a string and replaces all `"` symbols
# with `'` and vise versa.

user_string = input('Input your string:\n% ')

# temp = []

# for string in user_string.split("'"):
#     temp.append(string.replace('"', "'"))

# res = '"'.join(temp)

# print(res)


def quotes_replace(s: str) -> str:

    return '"'.join([part.replace('"', "'") for part in s.split("'")])


res = quotes_replace(user_string)

print(res)
