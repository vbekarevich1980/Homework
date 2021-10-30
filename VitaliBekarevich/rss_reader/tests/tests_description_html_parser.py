"""
This module contains unit tests for description_html_parser.py module.

"""

import unittest

from rss_reader_p import description_html_parser


class DescriptionHTMLParserClassTestCase(unittest.TestCase):
    def setUp(self):
        self.description_html_parser = \
            description_html_parser.DescriptionHTMLParser()

    def test_class_init(self):
        self.assertIsInstance(self.description_html_parser.parsed_links, set,
                              'not a set')
        self.assertIsInstance(self.description_html_parser.parsed_images, set,
                              'not a set')
        self.assertEqual(self.description_html_parser.parsed_text_data, '',
                         'parsed_text_data is set incorrectly')


if __name__ == '__main__':
    unittest.main()
