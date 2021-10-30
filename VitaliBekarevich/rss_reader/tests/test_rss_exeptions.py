"""
This module contains unit tests for rss_exceptions.py module.

"""

import unittest

from rss_reader_p import rss_exceptions


class RSSExceptionClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_exception = rss_exceptions.RSSException('message')

    def test_class_init(self):
        self.assertEqual(self.rss_exception.error_message, 'message',
                         'error_message is set incorrectly')


class NotRSSFeedErrorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.not_rss_feed_error = rss_exceptions.NotRSSFeedError('message')

    def test_class_str(self):
        self.assertEqual(str(self.not_rss_feed_error),
                         'NotRSSFeedError: message',
                         'error_message is set incorrectly')


class DateNotValidErrorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.date_not_valid_error = rss_exceptions.DateNotValidError('message')

    def test_class_str(self):
        self.assertEqual(str(self.date_not_valid_error),
                         'DateNotValidError: message',
                         'error_message is set incorrectly')


class NoCachedRSSFeedFoundErrorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.no_cached_rss_feed_found_error = \
            rss_exceptions.NoCachedRSSFeedFoundError('message')

    def test_class_str(self):
        self.assertEqual(str(self.no_cached_rss_feed_found_error),
                         'NoCachedRSSFeedFoundError: message',
                         'error_message is set incorrectly')


class RSSConnectionErrorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_connection_error = \
            rss_exceptions.RSSConnectionError('message')

    def test_class_str(self):
        self.assertEqual(str(self.rss_connection_error),
                         'RSSConnectionError: message',
                         'error_message is set incorrectly')


class RSSParserErrorClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_parser_error = \
            rss_exceptions.RSSParserError('message')

    def test_class_str(self):
        self.assertEqual(str(self.rss_parser_error),
                         'RSSParserError: message',
                         'error_message is set incorrectly')


if __name__ == '__main__':
    unittest.main()
