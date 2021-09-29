# Task 5.4
# Look through file `modules/legb.py`.
#
# 1) Find a way to call `inner_function` without moving it from inside of `enclosed_function`.
#
a = "I am global variable!"


def enclosing_function():
    a = "I am variable from enclosed function!"

    def inner_function():

        a = "I am local variable!"
        print(a)

    return inner_function()


enclosing_function()

# 2.1) Modify ONE LINE in `inner_function` to make it print variable 'a' from global scope.
#
a = "I am global variable!"


def enclosing_function():
    a = "I am variable from enclosed function!"

    def inner_function():

        global a
        print(a)

    return inner_function()


enclosing_function()

# 2.2) Modify ONE LINE in `inner_function` to make it print variable 'a' from enclosing function.
a = "I am global variable!"


def enclosing_function():
    a = "I am variable from enclosed function!"

    def inner_function():

        # a = "I am local variable!"
        print(a)

    return inner_function()


enclosing_function()
