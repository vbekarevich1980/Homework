# Task 1.3
# Write a Python program that accepts a comma separated sequence of words as input and prints the unique words
# in sorted form.
# Examples:
#
# Input: ['red', 'white', 'black', 'red', 'green', 'black']
# Output: ['black', 'green', 'red', 'white']

words_sequence = input('Input your comma separated sequence of words:\n% ').split(', ')

result = list(set(words_sequence))
result.sort()

print(result)

