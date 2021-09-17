# Task 1.1
# Write a Python program to calculate the length of a string without using the `len` function.

user_string = input('Input your string:\n% ')

# Method 1
i = 0
for char in user_string:
    i += 1

print(f'The string "{user_string}" consists of {i} chars.')

# Method 2
print(f'The string "{user_string}" consists of {user_string.rindex(user_string[-1]) + 1} chars.')
