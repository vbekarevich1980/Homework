# Task 1.6 (1.7)
# Write a Python program to convert a given tuple of positive integers into an integer.
# Examples:

# Input: (1, 2, 3, 4)
# Output: 1234

user_tuple = (1, 2, 3, 4)

# Method 1
result_int = int(''.join([str(digit) for digit in user_tuple]))

print(result_int)
print(type(result_int))

# Method 2
result_char_list = [str(digit) for digit in user_tuple]
result_str = ''.join(result_char_list)
result_int = int(result_str)

print(result_int)
print(type(result_int))
