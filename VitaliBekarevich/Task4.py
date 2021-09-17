# Task 1.3 (1.4)
# Create a program that asks the user for a number and then prints out a list of all the [divisors]
# (https://en.wikipedia.org/wiki/Divisor) of that number.
# Examples:
#
# Input: 60
# Output: {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}

user_number = int(input('Input your number:\n% '))

divisors = [i for i in range(1, user_number + 1) if user_number % i == 0]

print(divisors)
