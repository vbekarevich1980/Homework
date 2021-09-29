# Task 5.3
# File `data/students.csv` stores information about students in [CSV](https://en.wikipedia.org/wiki/Comma-
# separated_values) format.
# This file contains the student’s names, age and average mark.
# 1) Implement a function which receives file path and returns names of top performer students
# ```python
# def get_top_performers(file_path, number_of_top_students=5):
#     pass
#
# print(get_top_performers("students.csv"))
# >>> ['Teresa Jones', 'Richard Snider', 'Jessica Dubose', 'Heather Garcia', 'Joseph Head']
# ```
#
# 2) Implement a function which receives the file path with students info and writes CSV student information to the new
# file in descending order of age.
# Result:
# ```
# student name,age,average mark
# Verdell Crawford,30,8.86
# Brenda Silva,30,7.53
# ...
# Lindsey Cummings,18,6.88
# Raymond Soileau,18,7.27
# ```

import pandas as pd


def get_top_performers(file_path: str, number_of_top_students: int = 5) -> list:

    students = pd.read_csv(file_path)
    students.sort_values(by='average mark', inplace=True, ascending=False)

    return [students.iat[i, 0] for i in range(number_of_top_students)]


def get_sorted_by_age(file_path: str) -> None:

    students = pd.read_csv(file_path)
    students.sort_values(by='age', inplace=True, ascending=False)

    with open('data/sorted_students.csv', 'w') as new_file:
        students.to_csv(new_file)


print(get_top_performers('data/students.csv', 7))
get_sorted_by_age('data/students.csv')
