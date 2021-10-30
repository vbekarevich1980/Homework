"""
This module contains unit tests for rss.py module.

"""

import unittest
import xml
import os.path

from rss_reader_p import rss
from rss_reader_p.rss_exceptions import *


class NewsReaderClassTestCase(unittest.TestCase):
    def setUp(self):
        self.news_reader = rss.NewsReader('https://news.yahoo.com/rss/', 5)

    def test_class_init(self):
        self.assertIsInstance(self.news_reader, rss.NewsReader,
                              'not a NewsReader instance')
        self.assertEqual(self.news_reader.feed, '',
                         'not an empty string')
        self.assertIsInstance(self.news_reader.items, list,
                              'not a list')
        self.assertEqual(self.news_reader.items_limit, 5,
                         'not equals the set value of 5')
        self.assertEqual(self.news_reader.url, 'https://news.yahoo.com/rss/',
                         'not equals the set value of '
                         '"https://news.yahoo.com/rss/"')

    def test_class_iter(self):
        self.assertIsInstance(
            self.news_reader.__iter__(), rss.NewsViewer,
            'not a NewsViewer instance')


class NewsViewerClassTestCase(unittest.TestCase):
    def setUp(self):
        self.news_viewer = rss.NewsViewer([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)

    def test_class_init(self):
        self.assertIsInstance(self.news_viewer, rss.NewsViewer,
                              'not a NewsViewer instance')
        self.assertEqual(self.news_viewer.items, [1, 2, 3, 4, 5, 6, 7, 8, 9],
                         'not equals the specified list')
        self.assertEqual(self.news_viewer.offset, 0,
                         'equals the default offset - 0')
        self.assertEqual(self.news_viewer.items_limit, 5,
                         'equals the specified limit - 5')

    def test_class_next(self):
        self.assertEqual(next(self.news_viewer), 1,
                         'not equals the first element of the list - 1')
        self.assertEqual(self.news_viewer.offset, 1,
                         'not equals the correct offset - 1')

        self.news_viewer.offset = 5
        self.assertRaises(StopIteration, self.news_viewer.__next__)


class RSSNewsReaderClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_news_reader = rss.RSSNewsReader('https://news.yahoo.com/rss/')

    def test_class_init(self):
        self.assertIsInstance(self.rss_news_reader, rss.RSSNewsReader,
                              'not a RSSNewsReader instance')
        self.assertIsInstance(self.rss_news_reader.structure,
                              xml.etree.ElementTree.Element,
                              'not an ElementTree.Element instance')
        self.assertEqual(self.rss_news_reader.version, '2.0',
                         'the version of RSS was retrieved incorrectly')
        self.assertEqual(self.rss_news_reader.feed,
                         'Yahoo News - Latest News & Headlines',
                         'the title of the RSS feed was retrieved incorrectly')
        self.assertIsInstance(self.rss_news_reader.items, list, 'not a list')
        self.assertEqual(self.rss_news_reader.items_limit,
                         len(self.rss_news_reader.items),
                         'the end index is not limited by the number of items')
        self.rss_news_reader = rss.RSSNewsReader('https://news.yahoo.com/rss/',
                                                 1000)
        self.assertEqual(self.rss_news_reader.items_limit,
                         len(self.rss_news_reader.items),
                         'the end index is not limited by the number of items')
        self.rss_news_reader = rss.RSSNewsReader('https://news.yahoo.com/rss/',
                                                 3)
        self.assertEqual(self.rss_news_reader.items_limit, 3,
                         'the end index is not limited by the --limit option')

    def test_class_get_rss_structure(self):
        self.assertIsInstance(
            self.rss_news_reader._RSSNewsReader__get_rss_structure(),
            xml.etree.ElementTree.Element,
            'not an ElementTree instance')
        self.rss_news_reader.url = 'https://news'
        self.assertRaises(
            RSSConnectionError,
            self.rss_news_reader._RSSNewsReader__get_rss_structure)
        self.rss_news_reader.url = 'https://news.yahoo.com'
        self.assertRaises(
            RSSParserError,
            self.rss_news_reader._RSSNewsReader__get_rss_structure)
        self.rss_news_reader.url = 'https://www.w3.org/1999/xhtml/'
        self.assertRaises(
            NotRSSFeedError,
            self.rss_news_reader._RSSNewsReader__get_rss_structure)

    def test_class_set_items(self):
        self.assertIsInstance(
            self.rss_news_reader._RSSNewsReader__set_items(), list,
            'not a list instance')
        self.assertIsInstance(
            self.rss_news_reader._RSSNewsReader__set_items()[0], rss.RSSItem,
            'not a RSSItem instance')

    def test_class_cash_news_items(self):
        self.assertTrue(
            os.path.isfile(os.path.join('..', 'docs',
                                        'requested_news_storage.csv')),
            'no file created')


class RSSItemClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_item = rss.RSSItem(
            'Yahoo News - Latest News & Headlines',
            'https://news.yahoo.com/rss/',
            'title',
            'publish_date',
            'link')

    def test_class_init(self):
        self.assertIsInstance(self.rss_item, rss.RSSItem,
                              'not a RSSItem instance')
        self.assertEqual(self.rss_item.feed,
                         'Yahoo News - Latest News & Headlines',
                         'the title of the RSS feed was set incorrectly')
        self.assertEqual(self.rss_item.feed_url,
                         'https://news.yahoo.com/rss/',
                         'the URL of the RSS feed was set incorrectly')

    def test_class_set_title(self):
        self.assertEqual(self.rss_item.title,
                         'title',
                         'the title of the news item was set incorrectly')

    def test_class_set_publish_date(self):
        self.assertEqual(self.rss_item.publish_date,
                         'publish_date',
                         'the publishing date of the news item was set '
                         'incorrectly')

    def test_class_set_link(self):
        self.assertEqual(self.rss_item.link,
                         'link',
                         'the URL of the news item was set incorrectly')

    def test_class_set_description(self):
        self.assertIsNone(
            self.rss_item.description,
            'the description of the news item was set incorrectly')
        self.rss_item = \
            rss.RSSNewsReader('https://people.onliner.by/feed').items[0]
        self.assertIsInstance(self.rss_item.description,
                              rss.RSSItemDescription,
                              'not a RSSItemDescription instance')


class RSSItemDescriptionClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss_item_description =\
            (rss.RSSNewsReader('https://people.onliner.by/feed').
             items[0].description)

    def test_class_set_description(self):
        self.assertIsInstance(self.rss_item_description.description_text, str,
                              'not a string')
        self.assertIsInstance(self.rss_item_description.description_links,
                              list, 'not a list')
        self.assertIsInstance(self.rss_item_description.description_images,
                              list, 'not a list')

    def test_class_set_extension(self):
        self.assertIsInstance(self.rss_item_description.description_extension,
                              str, 'not a string')


if __name__ == '__main__':
    unittest.main()
