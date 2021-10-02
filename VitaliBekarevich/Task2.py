# Task 7.2
# Implement context manager for opening and working with file, including handling exceptions with @contextmanager
# decorator.

from contextlib import contextmanager


@contextmanager
def file_manager(file_path, mode):
    print('I am opening the file', file_path, 'in the mode', mode)
    file = open(file_path, mode)
    try:
        yield file
    except IOError:
        print(IOError, ': The wrong mode chosen!')
    finally:
        print('I am closing the file', file_path, '\n')
        file.close()


with file_manager('file.txt', 'w') as f:
    f.write('Some text')
    some_text = f.read()

with file_manager('file.txt', 'r') as f:
    # f.write('Some text')
    some_text1 = f.read()
    print('The text from the file:', some_text1)

with file_manager('file.txt', 'r') as f:
    some_text2 = f.read()
    print('The text from the file:', some_text2)
