"""
This module exports custom exceptions which can occur when
rss_reader.py utility running.

class RSSException -- the base class for all custom exceptions
class NotRSSFeedError -- the subclass of RSSException raised when not-rss
                      url parsing is attempted
class DateNotValidError -- the subclass of RSSException raised when the user
                      tries to get cached news published on the specified
                      date and such news of this date are not found
class NoCachedRSSFeedFoundError -- the subclass of RSSException raised
                      when the user tries to get cached news from
                      the specified RSS feed and such news from this date
                      are not found
class RSSConnectionError -- the subclass of RSSException raised when any type
                      of requests.exceptions.RequestException is raised
class RSSParserError -- the subclass of RSSException raised when
                      ElementTree.ParseError is raised and ElementTree.Parser
                      fails to recognise the data structure got from the URL
                      specified by the user
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

    def __str__(self):
        """
        Override __str__ of the superclass RSSException to set a
        representation of the class instance in stdout.

        :return: str
        The name of the error and the text of the error message
        """
        return 'NotRSSFeedError: ' + self.error_message


class DateNotValidError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    raised when no news published on the specified date are found in the
    local storage.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __str__ of the superclass RSSException to set a
        representation of the class instance in stdout.

        :return: str
        The name of the error and the text of the error message
        """
        return 'DateNotValidError: ' + self.error_message


class NoCachedRSSFeedFoundError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    raised when no news from the specified RSS are found in the
    local storage.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __str__ of the superclass RSSException to set a
        representation of the class instance in stdout.

        :return: str
        The name of the error and the text of the error message
        """
        return 'NoCachedRSSFeedFoundError: ' + self.error_message


class RSSConnectionError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    used to intercept any type of requests.exceptions.RequestException.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __str__ of the superclass RSSException to set a
        representation of the class instance in stdout.

        :return: str
        The name of the error and the text of the error message
        """
        return 'RSSConnectionError: ' + self.error_message


class RSSParserError(RSSException):
    """
    A subclass of RSSException to specify a special type of RSSException
    used to intercept ElementTree.ParseError if ElementTree.Parser
    fails to recognise the data structure got from the URL specified by
    the user.
    All methods are inherited from RSSException.
    """

    def __str__(self):
        """
        Override __str__ of the superclass RSSException to set a
        representation of the class instance in stdout.

        :return: str
        The name of the error and the text of the error message
        """
        return 'RSSParserError: ' + self.error_message
