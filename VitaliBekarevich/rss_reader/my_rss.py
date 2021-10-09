"""
This module exports MyRSS and MyRSSItem classes presenting containers for
a rss document.

class RSS -- the class for containing the parsed structure of a rss document
class RSSItem -- the class for containing the parsed structure of
a rss channel item
"""

import requests
import json
import html
import defusedxml.ElementTree as ElementTree
from .rss_exceptions import *
from .my_html_parser import DescriptionHTMLParser


class RSS:
    """
    A class used to represent a RSS container for the parsed structure of
    a rss document.

    Attributes
    ----------
    structure : xml.etree.ElementTree.Element
        the instance of Element class from defusedxml.ElementTree defining
        the root element of the parsed rss tree
    version : str
        string with the version of Really Simple Syndication (RSS) format
        used in the rss document
    title : str
        the name of the rss feed
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object of RSS
        by __next__ method
    offset : int
        the current position in the sequence of items of the __next__
        method in the iterator
    """

    def __init__(self, rss_url, items_limit=None):
        """
        Construct an instance of RSS class and set values for structure,
        version, title, items, items_limit, offset
        attributes.

        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :param items_limit: int
        The number of items to yield from iterator object of RSS
        by __next__ method (default is None)
        """
        self.structure = self.__get_rss_structure(rss_url)
        self.version = self.structure.attrib['version']
        self.title = self.structure[0].find('title').text
        self.items = self.__set_items()
        self.items_limit = items_limit if items_limit else len(self.items)
        self.offset = 0

    def __get_rss_structure(self, rss_url):
        """
        Get the instance of Element class from defusedxml.ElementTree
        defining the root element of the parsed rss tree.

        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :raise NotRSSFeedError
        If rss_url does not contain a rss feed
        :return: xml.etree.ElementTree.Element
        The instance of Element class from defusedxml.ElementTree
        defining the root element of the parsed rss tree
        """
        try:
            rss_request = requests.get(rss_url)
            rss_request.raise_for_status()
        except requests.HTTPError:
            print(f'Your request to {rss_url} returned an unsuccessful status '
                  f'code - {rss_request.status_code}. Please, try again later '
                  f'or use other link.')
        except ConnectionError:
            print(f'When trying to get {rss_url} some network problem '
                  f'occurred. Please, try again later.')
        except TimeoutError:
            print(f'Your request to {rss_url} timed out. Please, try again '
                  f'later.')
        except requests.TooManyRedirects:
            print(f'Your request to {rss_url} exceeded the number of maximum '
                  f'redirections. Please, try again later.')
        else:
            try:
                rss_structure = ElementTree.fromstring(rss_request.text)
            except ElementTree.ParseError:
                print(f'The data structure from {rss_url} failed to be '
                      f'recognise. Please, use other link.')
            else:
                if rss_structure.tag == 'rss':
                    return rss_structure
                else:
                    raise NotRSSFeedError(f'Your request to {rss_url} '
                                          f'returned not a RSS feed. '
                                          f'Please, try other link.')

    def __set_items(self):  # TODO Add flags from parameters - a JSON should
        # be created only if the lag is on
        """
        Generate a list of RSSItem instances.

        :return: list
        The list of RSSItem instances
        """
        rss_items = []

        for item in self.structure[0].findall('item'):
            title = item.find('title')
            publish_date = item.find('pubDate')
            link = item.find('link')
            description = item.find('description')
            rss_items.append(RSSItem(title, publish_date, link, description))
        return rss_items

    def __iter__(self):
        """
        Return the instance of RSS class as an iterator.

        :return: RSS
        The the instance of RSS class as an iterator
        """
        return self

    def __next__(self):
        """
        Return successive items in the list of RSSItem instances.

        :return: RSSItem
        The instance of RSSItem from the list stored in the 'items'
        attribute of a RSS instance
        """
        if self.offset >= self.items_limit:
            raise StopIteration
        else:
            item = self.items[self.offset]
            self.offset += 1
            return item


class RSSItem:
    """
    A class used to represent a RSSItem container for the parsed
    structure of a rss channel item.

    Attributes
    ----------
    title : str
        the item's headline (default is None)
    publish_date : str
        the publication date and time of the item (default is None)
    link : str
        the URL of a web page associated with the item (default is None)
    description : RSSItemDescription
        the RSSItemDescription instance (default is None)
    json : JSON formatted str
        the item presented by a JSON formatted str
    """

    def __init__(self, title=None, publish_date=None, link=None,
                 description=None):
        """
        Construct an instance of RSSItem class and set values for title,
        publish_date, link, description, _json
        attributes.

        :param title: str
        The item's headline (default is None)
        :param publish_date: str
        The publication date and time of the item (default is None)
        :param link: str
        The URL of a web page associated with the item (default is None)
        :param description: str
        The HTML text of the description part of the rss channel item
        (default is None)
        """
        self.title = None if title is None else html.unescape(title.text)
        self.publish_date = None if publish_date is None else publish_date.text
        self.link = None if link is None else link.text
        self.description = (None if description is None
                            else RSSItemDescription(description))
        self.json = self.__generate_json()

    def __generate_json(self):
        """
        Serialize a RSSItem object to a JSON formatted str.
        :return: JSON formatted str
        The item presented by a JSON formatted str
        """
        return json.dumps(
            {
                "title": self.title,
                "pubDate": self.publish_date,
                "link": self.link,
                "description": {
                    "text": (None if self.description is None
                             else self.description.description_text),
                    "links": (None if self.description is None
                              else self.description.description_links),
                    "images": (None if self.description is None
                               else self.description.description_images),
                },
            },
            indent=4,
            ensure_ascii=False
        )


class RSSItemDescription:
    """
    A class used to represent a RSSItemDescription container for
    the parsed structure of a rss channel item description.

    Attributes
    ----------
    description_text : str
        the text data parsed from HTML text of the rss channel item
        description
    description_links : list
        the list of URLs met in the rss channel item description
    description_images : list
        the list of URLs to images met in the rss channel item description
    description_extension : str
        the compiled from description_links and description_images text
        for printing out in stdout
    """

    def __init__(self, description):
        """
        Construct an instance of RSSItemDescription class and set values
        for description_text, description_links, description_images,
        description_extension attributes.

        :param description: str
        The HTML text of the description part of the rss channel item
        """
        (self.description_text,
         self.description_links,
         self.description_images) = self.__set_description(description)
        self.description_extension = self.__compile_extension()

    def __set_description(self, description):
        """
        Parse the text data and URLs from the HTML text of the description
         part of the rss channel item.

        :param description: description: str
        The HTML text of the description part of the rss channel item
        :return: tuple
        The text data parsed from HTML text of the rss channel item
        description
        The list of URLs met in the rss channel item description
        The list of URLs to images met in the rss channel item description
        """
        description_parser = DescriptionHTMLParser()
        description_parser.feed(description.text)
        text = description_parser.parsed_text_data
        links = list(description_parser.parsed_links)
        images = list(description_parser.parsed_images)

        return text, links, images

    def __compile_extension(self):
        """
        Compiled the string with the text for printing out in stdout
        from description_links and description_images.

        :return: str
        The compiled from description_links and description_images text for
        printing out in stdout
        """
        description_extension = 'Links:\n'
        line_number = 1
        for link in self.description_links:
            new_line = '[' + str(line_number) + ']: ' + link + ' (link)\n'
            description_extension += new_line
            line_number += 1
        for image in self.description_images:
            new_line = '[' + str(line_number) + ']: ' + image + ' (image)\n'
            description_extension += new_line
            line_number += 1

        return description_extension
