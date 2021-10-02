# Task 7.1
# Implement class-based context manager for opening and working with file, including handling exceptions. Do not use
# 'with open()'. Pass filename and mode via constructor.

class ContextManager:
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode

    def __enter__(self):
        self.file_object = open(self.file_path, self.mode)
        return self.file_object

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val.__class__.__name__ == 'UnsupportedOperation':
            print('The wrong mode chosen. The file is', exc_val, '!')
        self.file_object.close()
        print('The file is closed!\n')
        return True  # not to raise the exception outside 'with'


with ContextManager('file.txt', 'w') as file:
    file.write('Some text')
    some_text = file.read()

with ContextManager('file.txt', 'r') as file:
    file.write('Some text')
    some_text1 = file.read()
    print('The text from the file:', some_text1)

with ContextManager('file.txt', 'r') as file:
    some_text2 = file.read()
    print('The text from the file:', some_text2)
