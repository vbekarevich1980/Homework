# Task 4.3
# Implement a function which works the same as `str.split` method
# (without using `str.split` itself, of course).

def string_split(s: str, *, sep: str = None, max_split: int = -1) -> list:

    if sep is None:
        s = s.lstrip()

    splits = s.count(sep or ' ') if max_split < 0 else min(max_split, s.count(sep or ' '))

    res = []

    for i in range(splits + 1):

        if splits > 0:
            sep_pos = s.find(sep or ' ')
            if sep_pos >= 0:
                if s[:sep_pos] or sep is not None:
                    res.append(s[:sep_pos])

                if sep is None:
                    s = s[sep_pos + len(sep or ' '):].lstrip()
                else:
                    s = s[sep_pos + len(sep or ' '):]
            else:
                if sep is None and s.lstrip():
                    res.append(s.lstrip())
                elif sep is not None:
                    res.append(s)
        elif s or sep is not None:
            res.append(s)

        splits -= 1

    return res


user_string = input('Input your string:\n% ')

print(string_split(user_string, max_split=-1))
print(user_string.split(maxsplit=-1))
print(string_split(user_string, max_split=-1) == user_string.split(maxsplit=-1))
