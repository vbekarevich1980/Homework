"""
This module exports custom exceptions to errors which can occur during
rss_reader.py utility running.

class RSSException -- the base class for all custom exceptions
class NotRSSFeedError -- the subclass of RSSException raised when not-rss
url parsing is attempted
"""


class RSSException(Exception):
    """
    A class used to represent a RSSException.

    Attributes
    ----------
    error_message : str
        the text of the error message
    """

    def __init__(self, error_message):
        """
        Override __init__ of the superclass Exception to set an error message.

        :param error_message: str
        The text of the error message
        """
        self.error_message = error_message




class NotRSSFeedError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    raised when not-rss url parsing is attempted.
    All methods are inherited from RSSException.
    """

    pass

class DateNotValidError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    raised when not-rss url parsing is attempted.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __init__ of the superclass Exception to set an error message.

        :param error_message: str
        The text of the error message
        """
        return 'DateNotValidError: ' + self.error_message

class NoCachedRSSFeedFoundError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    raised when not-rss url parsing is attempted.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __init__ of the superclass Exception to set an error message.

        :param error_message: str
        The text of the error message
        """
        return 'NoCachedRSSFeedFoundError: ' + self.error_message
