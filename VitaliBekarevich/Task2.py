# Task 5.2
# Implement a function which search for most common words in the file.
# Use `data/lorem_ipsum.txt` file as a example.
#
# ```python
# def most_common_words(filepath, number_of_words=3):
#     pass
#
# print(most_common_words('lorem_ipsum.txt'))
# >>> ['donec', 'etiam', 'aliquam']
# ```
#
# > NOTE: Remember about dots, commas, capital letters etc.

import collections
from string import punctuation


def most_common_words(filepath: str, number_of_words: int = 3) -> list:

    word_counter = collections.Counter()

    with open(filepath) as f:
        text = f.read()

    word_list = text.split()

    for word in word_list:
        for symbol in punctuation:
            word = word.strip(symbol)
        word_counter[word] += 1

    return [item[0] for item in word_counter.most_common(number_of_words)]


print(most_common_words('data/lorem_ipsum.txt'))
