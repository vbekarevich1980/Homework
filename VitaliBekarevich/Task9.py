# Task 7.9
# Implement an iterator class EvenRange, which accepts start and end of the interval as an init arguments and gives
# only even numbers during iteration.
# If user tries to iterate after it gave all possible numbers `Out of numbers!` should be printed.
# _Note: Do not use function `range()` at all_
# Example:
# ```python
# er1 = EvenRange(7,11)
# next(er1)
# >>> 8
# next(er1)
# >>> 10
# next(er1)
# >>> "Out of numbers!"
# next(er1)
# >>> "Out of numbers!"
# er2 = EvenRange(3, 14)
# for number in er2:
#     print(number)
# >>> 4 6 8 10 12 "Out of numbers!"
# ```
class EvenRange:
    def __init__(self, start, end):
        self.value = start if start % 2 == 0 else start + 1
        self.end = end
        self.iterator_on = False

    def __iter__(self):
        self.iterator_on = True
        return self

    def __next__(self):
        if self.value >= self.end and self.iterator_on:
            print('Out of numbers!')
            raise StopIteration
        elif self.value >= self.end:
            return 'Out of numbers!'
        else:
            item = self.value
            self.value += 2
            return item


if __name__ == '__main__':
    er1 = EvenRange(7, 10)
    print(next(er1))
    print(next(er1))
    print(next(er1))
    print(next(er1))
    er2 = EvenRange(3, 16)
    for number in er2:
        print(number)
