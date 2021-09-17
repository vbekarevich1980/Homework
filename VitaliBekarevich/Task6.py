# Task 1.5 (1.6)
# Write a Python program to print all unique values of all dictionaries in a list.
# Examples:

# Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
# Output: {'S005', 'S002', 'S007', 'S001', 'S009'}

dict_list = [
    {"V": "S001", "VII": "S006"},
    {"V": "S002"},
    {"VI": "S001"},
    {"VI": "S005"},
    {"VII": "S005"},
    {"V": "S009"},
    {"VIII": "S007"}]

unique_values = set()

for dict_item in dict_list:
    for key in dict_item.keys():
        unique_values.add(dict_item[key])

print(unique_values)

