"""
This module exports NewsReader, NewsViewer, RSSNewsReader,
CachedNewsReader, RSSItem and RSSItemDescription classes presenting
containers for the news retrieved from a rss feed.

class NewsReader -- the class for containing the parsed news items from
                    a rss feed
class NewsViewer -- the class for creating an iterator for multiple
                    iteration through a NewsReader instance
class RSSNewsReader -- the subclass of NewsReader for containing the news
                    items parsed from a rss feed
class CachedNewsReader -- the subclass of NewsReader for containing the
                    news items retrieved from the local storage
class RSSItem -- the class for containing the parsed structure of
                    a single rss feed news item
class RSSItemDescription -- the class for containing the parsed
                    structure of a description of a news item
"""

import logging
import requests
import json
import html
import os.path
import defusedxml.ElementTree as ElementTree
import pandas as pd
from io import StringIO

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak

from .rss_exceptions import *
from .description_html_parser import DescriptionHTMLParser
from .rss_logger import rss_logger

# Set the logger
logger = logging.getLogger(__name__)


class NewsReader:
    """
    A container class used to accumulate the currently parsed news items
    and output them in the way requested by the user with the options
    of the rss_reader.py utility.

    Attributes
    ----------
    url : str
        the URL of the parsed RSS feed
    feed : str
        the title of the parsed RSS feed
    parsed_text_data : str
        the text data parsed from HTML text of the rss channel item
        description
    """
    @rss_logger(logger)
    def __init__(self, rss_url=None, items_limit=None):
        """
        Construct an instance of NewsReader class and set values for structure,
        version, title, url, items, items_limit, offset
        attributes.

        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :param items_limit: int
        The number of items to yield from iterator object of RSS
        by __next__ method (default is None)
        """
        self.url = rss_url
        self.feed = ''
        self.items = []
        self.limit = items_limit


    @rss_logger(logger)
    def __iter__(self):
        """
        Return the instance of RSS class as an iterator.

        :return: RSS
        The the instance of RSS class as an iterator
        """
        return NewsViewer(self.items, self.items_limit)

    @rss_logger(logger)
    def news_to_console_printer(self):
        """
        Print into stdout the title of the rss feed and the news items
        below.

        :param args: argparse.Namespace
        The arguments intercepted by argparse from command line
        """
        print('-' * 100)
        for item in self:
            if item.feed:
                print('Feed:', item.feed)
                print('-' * 100)
            if item.title is not None:
                print('Title:', item.title)  # TODO check if there are any  #
                        # items
            if item.link is not None:
                print('Link:', item.link)
            if item.publish_date is not None:
                print('Date:', item.publish_date, '\n')
            if item.description is not None:
                if item.description.description_text:
                    print(item.description.description_text, '\n')
                if item.description.description_extension:
                    print(item.description.description_extension)
            print('-' * 100)

    @rss_logger(logger)
    def json_to_console_printer(self):
        """
        Print into stdout the title of the rss feed and the news items
        below.

        :param args: argparse.Namespace
        The arguments intercepted by argparse from command line
        """
        print('-' * 100)
        for item in self:
            print(item.json)
            print('-' * 100)

    @rss_logger(logger)
    def news_to_pdf_converter(self, path, date=''):
        """
        Print into stdout the title of the rss feed and the news items
        below.

        :param args: argparse.Namespace
        The arguments intercepted by argparse from command line
        """
        registerFont(TTFont('Times', 'Times.ttc'))
        #feed = '<para><strong><font size=15>Feed:</font></strong> <font size=15 fontName="Times">Люди Onlíner</font></para>'# + self.url

        divider_style = ParagraphStyle(name='Normal', fontName='Times',
                                       fontSize=16, spaceAfter=15)

        # Check if the specified by the user path exists, if it is a file.
        # Create a directory if needed
        path = os.path.normcase(path)
        if os.path.exists(path):
            if os.path.isdir(path):
                file = os.path.join(path, f'news_{self.feed}_{date}.pdf')
            elif os.path.isfile(path):
                file = path
        else:
            os.makedirs(path)
            file = os.path.join(path, f'news_{self.feed}_{date}.pdf')

        doc = SimpleDocTemplate(file, pagesize=A4)
        story = []

        for item in self:
            feed = f'<para><strong><font size=15>Feed:</font></strong> ' \
                   f'<font size=15 fontName="Times">{item.feed}</font></para>'
            story.append(Paragraph(feed))
            story.append(Paragraph('', divider_style))
            if item.title is not None:
                title = f'<para><strong>Title:</strong> ' \
                        f'<font fontName="Times">{item.title}</font></para>'
                story.append(Paragraph(title))
            if item.link is not None:
                link = f'<para><strong>Link:</strong> ' \
                       f'<font fontName="Times"><link color="blue">' \
                       f'{item.link}</link></font></para>'
                story.append(Paragraph(link))
            if item.publish_date is not None:
                publish_date = f'<para><strong>Date:</strong> ' \
                               f'<font fontName="Times">{item.publish_date}' \
                               f'</font></para>'
                story.append(Paragraph(publish_date))
                story.append(Paragraph('', divider_style))

            if item.description is not None:
                if item.description.description_images:
                    for image in item.description.description_images:
                        image_pdf = f'<para autoleading="min">' \
                                    f'<img src={image} valign="top"/>' \
                                    f'<br/><br/></para>'
                        story.append(Paragraph(image_pdf))

                if item.description.description_text:
                    description_text = f'<para autoleading="min">' \
                                       f'<font fontName="Times">' \
                                       f'{item.description.description_text}' \
                                       f'</font></para>'
                    story.append(Paragraph(description_text))

                if item.description.description_links:
                    link_label = '<para><strong>Links:</strong></para>'
                    story.append(Paragraph('', divider_style))
                    story.append(Paragraph(link_label))

                    for i in range(len(item.description.description_links)):
                        link = f'<para>[{i+1}]: <font fontName="Times">' \
                               f'<link color="blue">' \
                               f'{item.description.description_links[i]}' \
                               f'</link></font></para>'
                        story.append(Paragraph(link))

            story.append(PageBreak())

        doc.build(story)

    @rss_logger(logger)
    def news_to_html_converter(self, path, date=''):
        """
        Print into stdout the title of the rss feed and the news items
        below.

        :param args: argparse.Namespace
        The arguments intercepted by argparse from command line
        """

        json_list = [json.loads(item.json) for item in self]

        news_dataframe = pd.read_json(StringIO(json.dumps(json_list)),
                                      orient='records', encoding='utf-16')
        # Check if the specified by the user path exists, if it is a file.
        # Create a directory if needed
        path = os.path.normcase(path)
        if os.path.exists(path):
            if os.path.isdir(path):
                file = os.path.join(path, f'news_{self.feed}_{date}.html')
            elif os.path.isfile(path):
                file = path
        else:
            os.makedirs(path)
            file = os.path.join(path, f'news_{self.feed}_{date}.html')

        with open(file, 'w',
                  encoding='utf-16') as html_file:
            #news_dataframe.to_csv(log_file, sep=';', header=False, index=False,
            #                      encoding='utf-16')
            news_dataframe.to_html(buf=html_file, columns=None, col_space=None,
                              header=True, index=False, na_rep='NaN',
                              formatters=None, float_format=None,
                              sparsify=None, index_names=True, justify=None,
                              max_rows=None, max_cols=None,
                              show_dimensions=False, decimal='.',
                              bold_rows=True, classes=None, escape=True,
                              notebook=False, border=None, table_id=None,
                              render_links=True, encoding=None)




class NewsViewer:
    @rss_logger(logger)
    def __init__(self, items, limit):
        """

        :param items:
        :type items:
        :param limit:
        :type limit:
        """
        self.items = items
        self.offset = 0
        self.items_limit = limit

    @rss_logger(logger)
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

class RSSNewsReader(NewsReader):
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
    url : str
        the URL of the rss feed
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object of RSS
        by __next__ method
    offset : int
        the current position in the sequence of items of the __next__
        method in the iterator
    """

    @rss_logger(logger)
    def __init__(self, rss_url, items_limit=None):
        """
        Construct an instance of RSS class and set values for structure,
        version, title, url, items, items_limit, offset
        attributes.

        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :param items_limit: int
        The number of items to yield from iterator object of RSS
        by __next__ method (default is None)
        """
        NewsReader.__init__(self, rss_url, items_limit)
        self.structure = self.__get_rss_structure()
        self.version = self.structure.attrib['version']
        self.feed = self.structure[0].find('title').text
        self.items = self.__set_items()
        self.items_limit = (items_limit if items_limit and items_limit < len(
            self.items) else len(self.items))

    @rss_logger(logger)
    def __get_rss_structure(self):
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
            rss_request = requests.get(self.url)
            rss_request.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionError(f'Your request to {self.url} returned an unsuccessful status '
                  f'code - {rss_request.status_code}. Please, try again later '
                  f'or use other link.')
        except requests.exceptions.ConnectionError:
            #print(f'When trying to get {self.url} some network problem '
            #      f'occurred. Please, try again later.')
            raise ConnectionError(f'When trying to get {self.url} some network problem'
                                  f'occurred. Please, try again later.')
        except requests.exceptions.Timeout:
            raise ConnectionError(f'Your request to {self.url} timed out. Please, try again '
                  f'later.')
        except requests.exceptions.TooManyRedirects:
            raise ConnectionError(f'Your request to {self.url} exceeded the number of maximum '
                  f'redirections. Please, try again later.')
        else:
            try:
                rss_structure = ElementTree.fromstring(rss_request.text)
            except ElementTree.ParseError:
                raise ParserError(f'The data structure from {self.url} failed to be '
                      f'recognise. Please, use other link.')
            else:
                if rss_structure.tag == 'rss':
                    return rss_structure
                else:
                    raise NotRSSFeedError(f'Your request to {self.url} '
                                          f'returned not a RSS feed. '
                                          f'Please, try other link.')

    @rss_logger(logger)
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
            rss_items.append(RSSItem(self.feed, self.url, title, publish_date, link, description))
        return rss_items

    #def news_to_console_printer(self):
    #    """
    #    Print into stdout the title of the rss feed and the news items
    #    below.
#
    #    :param args: argparse.Namespace
    #    The arguments intercepted by argparse from command line
    #    """
    #    print('-' * 50)
    #    print('Feed:', self.feed)
    #    print('-' * 50)
#
    #    NewsReader.news_to_console_printer(self)

    #def news_to_pdf_converter(self):
    #    NewsReader.news_to_pdf_converter(self)

    #def json_to_console_printer(self):
    #    """
    #    Print into stdout the title of the rss feed and the news items
    #    below.
#
    #    :param args: argparse.Namespace
    #    The arguments intercepted by argparse from command line
    #    """
    #    print('-' * 50)
    #    print('Feed:', self.feed)
    #    print('-' * 50)
#
    #    NewsReader.json_to_console_printer(self)
#
    @rss_logger(logger)
    def cash_news_items(self):
        """

        :return:
        :rtype:
        """

        json_list = [json.loads(item.json) for item in self.items]

        news_dataframe = pd.read_json(StringIO(json.dumps(json_list)), orient='records', encoding='utf-16')
        # Add a column with the dates of news publishing in needed format
        publish_dates = pd.to_datetime(news_dataframe['pubDate']).dt.strftime('%Y%m%d')
        news_dataframe = news_dataframe.join(publish_dates, rsuffix='_formatted')

        with open(os.path.join('docs', 'requested_news_storage.csv'), 'a', encoding='utf-16') as log_file:
            news_dataframe.to_csv(log_file, sep=';', header=False, index=False,
                      encoding='utf-16')


class CachedNewsReader(NewsReader):
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
    url : str
        the URL of the rss feed
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object of RSS
        by __next__ method
    offset : int
        the current position in the sequence of items of the __next__
        method in the iterator
    """

    @rss_logger(logger)
    def __init__(self, rss_url, publish_date, items_limit=None):
        """
        Construct an instance of RSS class and set values for structure,
        version, title, url, items, items_limit, offset
        attributes.
        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :param items_limit: int
        The number of items to yield from iterator object of RSS
        by __next__ method (default is None)
        """
        NewsReader.__init__(self, rss_url, items_limit)
        self.feed = ''
        self.publish_date = publish_date
        self.items = self.__set_items()
        self.items_limit = (
            items_limit if items_limit and items_limit < len(
                self.items) else len(self.items))

    @rss_logger(logger)
    def __set_items(self):  # TODO Add flags from parameters - a JSON should
        # be created only if the lag is on
        """
        Generate a list of RSSItem instances.
        :return: list
        The list of RSSItem instances
        """
        rss_items = []



        cached_news = pd.read_csv(os.path.join('docs', 'requested_news_storage.csv'), sep=';',
                                  decimal=',', header=None,
                                  names=['feed', 'feed_url', 'title',
                                         'pubDate', 'link', 'description_text',
                                         'description_links',
                                         'description_images', 'pubDate_formatted'], usecols=[0, 1, 2, 3,4,5,6,7,8],
                                  parse_dates=['pubDate_formatted'], infer_datetime_format=True,
                                  skip_blank_lines=True, encoding='utf-16')


        cached_news.drop_duplicates(inplace=True)

        try:
            # Pick up the news by the date
            selected_by_date_news = cached_news.loc[
                cached_news['pubDate_formatted'] == self.publish_date]

            if selected_by_date_news.empty:
                raise DateNotValidError('There are no cached news published on the specified date. Please, try another date.')

            # Pick up the news by the feed
            if self.url:
                selected_by_date_and_feed_news = selected_by_date_news.loc[
                    selected_by_date_news['feed_url'] == self.url]
                if selected_by_date_and_feed_news.empty:
                    raise NoCachedRSSFeedFoundError(
                        'There are no cached news from the specified feed. '
                        'Please, try another URL.')
                self.feed = selected_by_date_and_feed_news.iat[0, 0]
                selected_news_json = selected_by_date_and_feed_news.to_json(orient='records', force_ascii=False)
            else:
                selected_news_json = selected_by_date_news.to_json(orient='records', force_ascii=False)

            selected_news = json.loads(selected_news_json)

            for item in selected_news:
                feed = item['feed']
                feed_url = item['feed_url']
                title = item["title"]
                publish_date = item["pubDate"]
                link = item["link"]
                description_text = item["description_text"]
                description_links = item["description_links"]
                description_images = item["description_images"]
                rss_items.append(
                    RSSItem(feed, feed_url, title, publish_date, link,
                            RSSItemDescription(text=description_text,links=description_links,images=description_images)))
        except DateNotValidError as error:
            print(error)
        except NoCachedRSSFeedFoundError as error:
            print(error)
        finally:
            return rss_items

    #def news_to_console_printer(self):
    #    """
    #    Print into stdout the title of the rss feed and the news items
    #    below.
#
    #    :param args: argparse.Namespace
    #    The arguments intercepted by argparse from command line
    #    """
    #    print('-' * 50)
    #    print('Feed:', self.feed)
    #    print('-' * 50)
#
    #    NewsReader.news_to_console_printer(self)
#
    #def json_to_console_printer(self):
    #    """
    #    Print into stdout the title of the rss feed and the news items
    #    below.
#
    #    :param args: argparse.Namespace
    #    The arguments intercepted by argparse from command line
    #    """
    #    print('-' * 50)
    #    print('Feed:', self.feed)
    #    print('-' * 50)
#
    #    NewsReader.json_to_console_printer(self)


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

    @rss_logger(logger)
    def __init__(self, feed, feed_url, title=None, publish_date=None, link=None,
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
        self.feed = feed
        self.feed_url = feed_url
        self.__set_title(title)
        self.__set_publish_date(publish_date)
        self.__set_link(link)
        self.__set_description(description)
        #self.description = (None if description is None
        #                    else RSSItemDescription(description=description))
        self.json = self.__generate_json()

    @rss_logger(logger)
    def __set_title(self, title):
        """

        :param title:
        :type title:
        :return:
        :rtype:
        """
        if title is None:
            self.title = None
        elif isinstance(title, str):
            self.title = title
        else:
            self.title = html.unescape(title.text)

    @rss_logger(logger)
    def __set_publish_date(self, publish_date):
        """

        :param publish_date:
        :type publish_date:
        :return:
        :rtype:
        """
        if publish_date is None:
            self.publish_date = None
        elif isinstance(publish_date, str):
            self.publish_date = publish_date
        else:
            self.publish_date = publish_date.text

    @rss_logger(logger)
    def __set_link(self, link):
        """

        :param link:
        :type link:
        :return:
        :rtype:
        """
        if link is None:
            self.link = None
        elif isinstance(link, str):
            self.link = link
        else:
            self.link = link.text

    @rss_logger(logger)
    def __set_description(self, description):
        """

        :param description:
        :type description:
        :return:
        :rtype:
        """
        if description is None:
            self.description = None
        elif isinstance(description, RSSItemDescription):
            self.description = description
        else:
            self.description = RSSItemDescription(description=description)

    @rss_logger(logger)
    def __generate_json(self):
        """
        Serialize a RSSItem object to a JSON formatted str.
        :return: JSON formatted str
        The item presented by a JSON formatted str
        """
        return json.dumps(
            {
                    "feed": self.feed,
                    "feed_url": self.feed_url,
                    "title": self.title,
                    "pubDate": self.publish_date,
                    "link": self.link,
                    "description_text":
                        (None if self.description is None
                         else self.description.description_text),
                    "description_links":
                        (None if self.description is None
                         else self.description.description_links),
                    "description_images":
                        (None if self.description is None
                         else self.description.description_images)
                }
            ,
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

    @rss_logger(logger)
    def __init__(self, *, description=None, text=None, links=None, images=None):
        """
        Construct an instance of RSSItemDescription class and set values
        for description_text, description_links, description_images,
        description_extension attributes.

        :param description: str
        The HTML text of the description part of the rss channel item
        """
        self.__set_description(description=description, text=text, links=links, images=images)
        self.__set_extension()

    @rss_logger(logger)
    def __set_description(self, **kwargs):
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
        #print(kwargs['description'])
        #print(type(kwargs['description']))
        #print('^^^^^^')
        if kwargs['description'] is not None:
            description_parser = DescriptionHTMLParser()
            description_parser.feed(kwargs['description'].text)
            self.description_text = description_parser.parsed_text_data
            self.description_links = list(description_parser.parsed_links)
            self.description_images = list(description_parser.parsed_images)
        else:
            self.description_text = kwargs['text'] if kwargs['text'] else ''
            # If the list of links is not empty
            if kwargs['links']:
                # Remove extra quotes
                self.description_links = [link.strip("'\"") for link in kwargs['links'].strip('[]').split(', ')]
            else:
                self.description_links = []
            #self.description_links = kwargs['links'].strip('[]').split(', ') \
            #    if kwargs['links'] else []
            # If the list of links is not empty
            if kwargs['images']:
                # Remove extra quotes
                self.description_images = [image.strip("'\"") for image in kwargs['images'].strip('[]').split(', ')]
            else:
                self.description_images =[]
                #self.description_images = kwargs['images'].strip('[]').split(', ')\
                #if kwargs['images'] else []

    @rss_logger(logger)
    def __set_extension(self):
        """
        Compiled the string with the text for printing out in stdout
        from description_links and description_images.

        :return: str
        The compiled from description_links and description_images text for
        printing out in stdout
        """

        if self.description_links or self.description_images:
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
        else:
            description_extension = ''

        self.description_extension = description_extension


