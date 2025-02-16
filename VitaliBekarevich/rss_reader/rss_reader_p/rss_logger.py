"""
This module exports rss_logger decorator for logging what the classes
methods do while the rss_reader.py utility running.

"""


def rss_logger(logger):
    """
    Decorate functions or method by adding logging the docstring into
    the stdout.

    :param logger: Logger
    The logger of the current module
    :return: wrapped function or method
    The callable object of the wrapped function or method
    """
    def rss_logging(function):
        """
        Decorate functions or method by adding logging the docstring into
        the stdout.

        """
        def wrapped(*args, **kwargs):
            """
            Add logging of a function or method performance, the first
            sentence of the docstring is used.

            :param args: any
            Any positional arguments passed to the wrapped function or method
            :param kwargs: any
            Any keyword arguments passed to the wrapped function or method
            :return: function or method
            The callable object of the function or method
            """
            # Parse the docstring of a function or method
            docstring = function.__doc__.split('.\n', maxsplit=1)[0].strip()
            # Set the first word, e.g. Do -> Doing, Handle -> Handling
            start_word = docstring.split(maxsplit=1)[0]
            if start_word.endswith('e'):
                start_word = start_word[:-1] + 'ing '
            elif start_word.endswith('ie'):
                start_word = start_word[:-2] + 'ying '
            elif start_word.endswith('l'):
                start_word = start_word + 'ling '
            elif start_word.endswith('ic'):
                start_word = start_word + 'king '
            else:
                start_word = start_word + 'ing '
            log = start_word + docstring.split(maxsplit=1)[1] + '.'
            logger.debug(log)
            return function(*args, **kwargs)
        return wrapped
    return rss_logging
