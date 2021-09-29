# Task 5.1
# Open file `data/unsorted_names.txt` in data folder. Sort the names and write them to a new file called
# `sorted_names.txt`. Each name should start with a new line as in the following example:
#
# ```
# Adele
# Adrienne
# ...
# Will
# Xavier
# ```

with open('data/unsorted_names.txt') as f:
    names = f.readlines()
    names.sort()

with open('data/sorted_names.txt', 'w') as new_f:
    new_f.writelines(names)
