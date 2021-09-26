# Task 4.6
# Implement a function `get_shortest_word(s: str) -> str` which returns the
# longest word in the given string. The word can contain any symbols except
# whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
# the string with a same length return the word that occurs first.
# Example:
# ```python
# >>> get_shortest_word('Python is simple and effective!')
# 'effective!'
# >>> get_shortest_word('Any pythonista like namespaces a lot.')
# 'pythonista'
# ```

def get_shortest_word(s: str) -> str:

    new_s = ''.join([char for char in s if char.isprintable()])
    length = 0
    split_s = new_s.split()

    for word in split_s:
        if len(word) > length:
            length = len(word)

    longest_words = [word for word in split_s if len(word) == length]

    return longest_words[0]


# user_string = input('Input your string:\n% ')
user_string = '\t\t\t\t\t\r12345 54321 12345 \n\n\n123\n\t34'
print(get_shortest_word(user_string))
