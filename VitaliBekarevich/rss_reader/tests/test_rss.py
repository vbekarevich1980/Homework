"""
This module contains unit tests for rss.py module.

class RSS -- the class for containing the parsed structure of a rss document
class RSSItem -- the class for containing the parsed structure of
a rss channel item
"""

import unittest
import xml
import requests
from rss_reader_p import rss


class RSSClassTestCase(unittest.TestCase):
    def setUp(self):
        self.rss = rss.RSS('https://news.yahoo.com/rss/')

    def test_class_init(self):
        self.assertIsInstance(self.rss, rss.RSS, 'not a RSS object')
        self.assertIsInstance(self.rss.structure,
                              xml.etree.ElementTree.Element,
                              'not an ElementTree object')
        self.assertEqual(self.rss.version, '2.0',
                         'the version of RSS was retrieved incorrectly')
        self.assertEqual(self.rss.title,
                         'Yahoo News - Latest News & Headlines',
                         'the title of the RSS feed was retrieved incorrectly')
        self.assertIsInstance(self.rss.items, list, 'not a list')
        self.assertEqual(self.rss.offset, 0,
                         'the start index is not set into "0"')
        self.assertEqual(self.rss.items_limit, len(self.rss.items),
                         'the end index is not limited by the number of items')

    def test_class_get_rss_structure(self):
        self.assertIsInstance(
            self.rss._RSS__get_rss_structure('https://news.yahoo.com/rss/'),
            xml.etree.ElementTree.Element,
            'not an ElementTree object')
        #with self.assertRaises(xml.p.ElementTree.ParseError):
        #    self.rss._RSS__get_rss_structure('https://news.yahoo.com')

    def test_class_iter(self):
        self.assertIs(self.rss.__iter__(), self.rss)

    def test_class_next(self):
        self.assertIs(self.rss.__next__(), self.rss.items[0])

if __name__ == '__main__':
    unittest.main()

"""., [11 окт. 2021 г., 19:30:36]:
у вас юнитом тестирования будет вероятнее всего отдельные методы класса

т.е. тест выглядит так. Подготовка: инстанциирование класса, установка необходимых полей, мок внешних зависимостей.

Выполнение действия - вызов тестируемого метода

assert - сравнение результата работы функции и ожидаемого"""