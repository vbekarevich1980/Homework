# Task 7.8
# Implement your custom iterator class called MySquareIterator which gives squares of elements of collection it
# iterates through.
# Example:
# ```python
# lst = [1, 2, 3, 4, 5]
# itr = MySquareIterator(lst)
# for item in itr:
#     print(item)
# >>> 1 4 9 16 25

class MySquareIterator:
    def __init__(self, collection):
        self.collection = collection
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.offset >= len(self.collection):
            raise StopIteration
        item = self.collection[self.offset] ** 2
        self.offset += 1
        return item


if __name__ == '__main__':
    lst = [1, 2, 3, 4, 5]
    itr = MySquareIterator(lst)
    for i in itr:
        print(i)
