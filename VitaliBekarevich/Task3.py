# Task 7.3
# Implement decorator with context manager support for writing execution time to log-file. See contextlib module.

from contextlib import ContextDecorator
from time import time, ctime


class executiontimelogging(ContextDecorator):
    def __enter__(self):
        self.time = time()
        return self

    def __exit__(self, *exc):
        with open('time_log.txt', 'a') as log:
            log.writelines(f'{ctime()}: The function was running for {time() - self.time} seconds.\n')
        return False


@executiontimelogging()
def function():
    print('I am doing something...')


function()
