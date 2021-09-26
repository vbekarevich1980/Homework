# Task 4.2
# Write a function that check whether a string is a palindrome or not. Usage of
# any reversing functions is prohibited. To check your implementation you can use
# strings from [here](https://en.wikipedia.org/wiki/Palindrome#Famous_palindromes).

def is_palindrome(s: str) -> bool:

    for char in [' ', ',', '.', '?', '!', '@', '(', ')', '_', ':', ';', "'", '"']:
        s = s.replace(char, '')

    return s == s[::-1]


user_string = input('Input your string:\n% ')

print(is_palindrome(user_string))
