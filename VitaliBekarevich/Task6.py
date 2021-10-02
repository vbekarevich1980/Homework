# Task 7.6
# Create console program for proving Goldbach's conjecture. Program accepts number for input and print result.
# For pressing 'q' program successfully close. Use function from Task 5.5 for validating input, handle all exceptions
# and print user friendly output.

from Task5 import *


def primes(number: int) -> list:

    primes_list = []

    for i in range(2, number + 1):
        for a_prime in primes_list:
            if i % a_prime == 0:
                break
        else:
            primes_list.append(i)
    return primes_list


def goldbach(number: int) -> tuple:

    if is_even(number):
        primes_list = primes(number)

        for a_prime in primes_list:
            if (number - a_prime) in primes_list:
                return a_prime, number - a_prime
        else:
            raise MyException("Goldbach's conjecture theory failed ;(")


def main():

    print("Welcome to'Goldbach's Conjecture Checker'!\n")

    while True:

        number = input("Please, enter an even integer greater than 2, \nor 'q' to quit.\n>>>> ")

        if number.lower() == 'q':
            break
        else:
            try:
                number = int(number)
                result = goldbach(number)
                print(f"\n{number} is the result of {result[0]} + {result[1]}.\nIt's proving Goldbach's conjecture.\n")
            except (ValueError, MyException):
                print('\nThe input does not correspond the program requirements.')

    print("\nYou are quitting 'Goldbach's Conjecture Checker'...\nSee you next time!")


if __name__ == '__main__':
    main()
