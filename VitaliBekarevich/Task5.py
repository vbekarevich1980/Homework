# Task 1.4 (1.5)
# Write a Python program to sort a dictionary by key.

import collections

user_dict = {'color': 'red',
             'mileage': 3812.4,
             'automatic': True,
             }

# Method 1
sorted_dict_from_collections = collections.OrderedDict()

for key in sorted(user_dict):
    sorted_dict_from_collections[key] = user_dict[key]

print(sorted_dict_from_collections)

# Method 2 (for Python 3.9)
sorted_dict_reg = {}

for key in sorted(user_dict):
    sorted_dict_reg[key] = user_dict[key]

print(sorted_dict_reg)

# Method 3 (for Python 3.9)
sorted_dict_reg = {key: user_dict[key] for key in sorted(user_dict)}

print(sorted_dict_reg)