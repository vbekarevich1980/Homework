# Task 7.7
# Implement your custom collection called MyNumberCollection. It should be able to contain only numbers. It should NOT
# inherit any other collections.
# If user tries to add a string or any non numerical object there, exception `TypeError` should be raised. Method init
# should be able to take either
# `start,end,step` arguments, where `start` - first number of collection, `end` - last number of collection or some
# ordered iterable
# collection (see the example).
# Implement following functionality:
# * appending new element to the end of collection
# * concatenating collections together using `+`
# * when element is addressed by index(using `[]`), user should get square of the addressed element.
# * when iterated using cycle `for`, elements should be given normally
# * user should be able to print whole collection as if it was list.
# Example:
# ```python
# col1 = MyNumberCollection(0, 5, 2)
# print(col1)
# >>> [0, 2, 4, 5]
# col2 = MyNumberCollection((1,2,3,4,5))
# print(col2)
# >>> [1, 2, 3, 4, 5]
# col3 = MyNumberCollection((1,2,3,"4",5))
# >>> TypeError: MyNumberCollection supports only numbers!
# col1.append(7)
# print(col1)
# >>> [0, 2, 4, 5, 7]
# col2.append("string")
# >>> TypeError: 'string' - object is not a number!
# print(col1 + col2)
# >>> [0, 2, 4, 5, 7, 1, 2, 3, 4, 5]
# print(col1)
# >>> [0, 2, 4, 5, 7]
# print(col2)
# >>> [1, 2, 3, 4, 5]
# print(col2[4])
# >>> 25
# for item in col1:
#     print(item)
# >>> 0 2 4 5 7
# ```
from numbers import Number
from numpy import arange


class MyNumberCollection:
    def __init__(self, *args):
        self.__set_iterable(*args)

    def __set_iterable(self, *args):
        """Setter for the iterable property."""
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            for element in args[0]:
                if not isinstance(element, Number):
                    raise TypeError('MyNumberCollection supports only numbers!')
            self.__iterable = [element for element in args[0]]
        else:
            for argument in args:
                if not isinstance(argument, Number):
                    raise TypeError('MyNumberCollection supports only numbers!')

            iterable_object = list(arange(*args))
            # Appending the last item (passed 'end' argument) as the arrange function skips it
            if len(args) == 1:
                iterable_object.append(args[0])
            else:
                iterable_object.append(args[1])

            self.__iterable = iterable_object

    def __get_iterable(self):
        """Getter for the iterable property."""
        return self.__iterable

    # Using the method 'property' to access the property through the dot operator (.)
    iterable = property(__get_iterable, __set_iterable)

    def __str__(self):
        return str(self.__iterable)

    def append(self, element):
        if isinstance(element, Number):
            self.__iterable.append(element)
        else:
            raise TypeError(f"'{element}' - object is not a number!")

    def __add__(self, other):
        return MyNumberCollection(self.__iterable + other.__iterable)

    def __getitem__(self, index):
        return self.__iterable[index] ** 2

    def __iter__(self):
        for element in self.__iterable:
            yield element


if __name__ == '__main__':
    col1 = MyNumberCollection(0, 5, 2)
    print(col1)
    col2 = MyNumberCollection((1, 2, 3, 4, 5))
    print(col2)
    # col3 = MyNumberCollection((1,2,3,"4",5))
    col1.append(7)
    print(col1)
    # col2.append("string")
    print(col1 + col2)
    print(col2 + col1)
    print(col1)
    print(col2)
    print(col2[4])
    for item in col1:
        print(item)
