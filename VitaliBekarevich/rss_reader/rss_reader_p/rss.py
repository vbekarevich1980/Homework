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
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object
    """

    @rss_logger(logger)
    def __init__(self, rss_url=None, items_limit=None):
        """
        Construct an instance of NewsReader class and set values for url,
        feed, items and items_limit attributes.

        :param rss_url: str
        The URL of the parsed RSS feed (default is None)
        :param items_limit: int
        The number of items to yield from iterator object (default is None)
        """
        self.url = rss_url
        self.feed = ''
        self.items = []
        self.items_limit = items_limit

    @rss_logger(logger)
    def __iter__(self):
        """
        Return the instance of NewsViewer class as an iterator.

        :return: NewsViewer
        The the instance of NewsViewer class as an iterator
        """
        return NewsViewer(self.items, self.items_limit)

    @rss_logger(logger)
    def news_to_console_printer(self):
        """
        Print into stdout the news items parsed from the RSS feed in
        standard format.

        """
        print('-' * 100)
        for item in self:
            if item.feed:
                print('Feed:', item.feed)
                print('-' * 100)
            if item.title is not None:
                print('Title:', item.title)
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
        Print into stdout the news items parsed from the RSS feed in
        JSON format.

        """
        print('-' * 100)
        for item in self:
            print(item.json)
            print('-' * 100)

    @rss_logger(logger)
    def news_to_pdf_converter(self, path, date=''):
        """
        Save the news items parsed from the RSS feed into a pdf file.

        :param path: str
        The path like string
        :param date: str
        The date like 'YYYYMMDD' string  (default is '')
        """
        # Register the font for the correct displaying of cyrillic
        registerFont(TTFont('Times', 'Times.ttc'))

        # Set a divider between the sections of the pdf file
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

            # Set the RSS feed title
            feed = f'<para><strong><font size=15>Feed:</font></strong> ' \
                   f'<font size=15 fontName="Times">{item.feed}</font></para>'
            story.append(Paragraph(feed))
            story.append(Paragraph('', divider_style))

            # Set the item title
            if item.title is not None:
                title = f'<para><strong>Title:</strong> ' \
                        f'<font fontName="Times">{item.title}</font></para>'
                story.append(Paragraph(title))

            # Set the item URL
            if item.link is not None:
                link = f'<para><strong>Link:</strong> ' \
                       f'<font fontName="Times"><link color="blue">' \
                       f'{item.link}</link></font></para>'
                story.append(Paragraph(link))

            # Set the item publishing date
            if item.publish_date is not None:
                publish_date = f'<para><strong>Date:</strong> ' \
                               f'<font fontName="Times">{item.publish_date}' \
                               f'</font></para>'
                story.append(Paragraph(publish_date))
                story.append(Paragraph('', divider_style))

            # Set the item description
            if item.description is not None:

                # Set the description images
                if item.description.description_images:
                    for image \
                            in enumerate(item.description.description_images):
                        # Try to load the description images
                        try:
                            image_request = requests.get(image[1])
                        # If loading failed set the description images as links
                        except requests.exceptions.RequestException:
                            image_pdf = f'<para>[{image[0] + 1}]: <font ' \
                                        f'fontName="Times">' \
                                        f'<link color="blue">{image[1]}' \
                                        f'</link> (image was not loaded)' \
                                        f'</font></para>'
                        else:
                            # If loading succeeded load the description images
                            # into the pdf file
                            if image_request.status_code == 200:
                                image_pdf = f'<para autoleading="min">' \
                                    f'<img src={image[1]} valign="top"/>' \
                                    f'<br/><br/></para>'
                        story.append(Paragraph(image_pdf))
                story.append(Paragraph('', divider_style))

                # Set the description text
                if item.description.description_text:
                    description_text = f'<para autoleading="min">' \
                                       f'<font fontName="Times">' \
                                       f'{item.description.description_text}' \
                                       f'</font></para>'
                    story.append(Paragraph(description_text))

                # Set the description links
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
            # Set a page break
            story.append(PageBreak())
        # Build a file
        doc.build(story)

    @rss_logger(logger)
    def news_to_html_converter(self, path, date=''):
        """
        Save the news items parsed from the RSS feed into a pdf file.

        :param path: str
        The path like string
        :param date: str
        The date like 'YYYYMMDD' string  (default is '')
        """
        # Load the news items JSON formatted
        json_list = [json.loads(item.json) for item in self]
        # Create a DataFrame from the list of the news items JSON formatted
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
        # Convert the DataFrame into a HTML file
        with open(file, 'w', encoding='utf-16') as html_file:
            news_dataframe.to_html(
                buf=html_file, columns=None, col_space=None,
                header=True, index=False, na_rep='NaN',
                formatters=None, float_format=None, sparsify=None,
                index_names=True, justify=None, max_rows=None,
                max_cols=None, show_dimensions=False, decimal='.',
                bold_rows=True, classes=None, escape=True,
                notebook=False, border=None, table_id=None,
                render_links=True, encoding=None)


class NewsViewer:
    """
    A class used to create an iterator object for multiple iteration
    through the parsed news items in a NewsReader instance.

    Attributes
    ----------
    items : list
        the list of RSSItem instances
    offset : int
        the current position in the sequence of items of the __next__ method
        in the iterator
    items_limit : int
        the number of items to yield from iterator object
    """

    @rss_logger(logger)
    def __init__(self, items, limit):
        """
        Construct an instance of NewsViewer class and set values for items,
        offset and items_limit attributes.

        :param items: str
        The list of RSSItem instances
        :param limit: int
        The number of items to yield from iterator object
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
        attribute of a NewsViewer instance
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
    a RSS feed.

    Attributes
    ----------
    structure : xml.etree.ElementTree.Element
        the instance of Element class from defusedxml.ElementTree defining
        the root element of the parsed rss tree
    version : str
        string with the version of Really Simple Syndication (RSS) format
        used in the rss document
    feed : str
        the title of the rss feed
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object
    """

    @rss_logger(logger)
    def __init__(self, rss_url, items_limit=None):
        """
        Construct an instance of RSSNewsReader class and set values for
        structure, version, feed, items and items_limit attributes.

        :param rss_url: str
        The URL string passed for retrieving a rss document from
        :param items_limit: int
        The number of items to yield from iterator object (default is None)
        """
        NewsReader.__init__(self, rss_url, items_limit)
        self.structure = self.__get_rss_structure()
        self.version = self.structure.attrib['version']
        self.feed = self.structure[0].find('title').text
        self.items = self.__set_items()
        self.items_limit = (items_limit
                            if items_limit and items_limit < len(self.items)
                            else len(self.items))

    @rss_logger(logger)
    def __get_rss_structure(self):
        """
        Get the instance of Element class from defusedxml.ElementTree
        defining the root element of the parsed rss tree.

        :raise RSSConnectionError
        If it is possible to connect the RSS URL
        :raise RSSParserError
        If the data structure from the RSS URL fails to be recognised
        :raise NotRSSFeedError
        If the RSS URL does not contain a RSS feed
        :return: xml.etree.ElementTree.Element
        The instance of Element class from defusedxml.ElementTree
        defining the root element of the parsed rss tree
        """
        # Try to connect to the RSS URL
        try:
            rss_request = requests.get(self.url)
            rss_request.raise_for_status()
        except requests.exceptions.HTTPError:
            raise RSSConnectionError(f'Your request to {self.url} returned '
                                     f'an unsuccessful status code - '
                                     f'{rss_request.status_code}. Please, '
                                     f'try again later or use other link.')
        except requests.exceptions.ConnectionError:
            raise RSSConnectionError(f'When trying to get {self.url} some '
                                     f'network problem occurred. Please, '
                                     f'try again later.')
        except requests.exceptions.Timeout:
            raise RSSConnectionError(f'Your request to {self.url} timed out. '
                                     f'Please, try again later.')
        except requests.exceptions.TooManyRedirects:
            raise RSSConnectionError(f'Your request to {self.url} exceeded '
                                     f'the number of maximum redirections. '
                                     f'Please, try again later.')
        # If succeeds try to get the RSS structure
        else:
            try:
                rss_structure = ElementTree.fromstring(rss_request.text)
            except ElementTree.ParseError:
                raise RSSParserError(f'The data structure from {self.url} '
                                     f'failed to be recognised. Please, use '
                                     f'other link.')
            # If succeeds check the tag of the structure for being a RSS feed
            else:
                if rss_structure.tag == 'rss':
                    return rss_structure
                else:
                    raise NotRSSFeedError(f'Your request to {self.url} '
                                          f'returned not a RSS feed. '
                                          f'Please, try other link.')

    @rss_logger(logger)
    def __set_items(self):
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
            rss_items.append(
                RSSItem(self.feed, self.url, title, publish_date, link,
                        description))
        return rss_items

    @rss_logger(logger)
    def cash_news_items(self):
        """
        Cache the RSS news items into the local storage.

        """
        # Load the news items JSON formatted
        json_list = [json.loads(item.json) for item in self.items]
        # Create a DataFrame from the list of the news items JSON formatted
        news_dataframe = pd.read_json(StringIO(json.dumps(json_list)),
                                      orient='records', encoding='utf-16')
        # Add a column with the dates of news publishing in needed format
        publish_dates = pd.to_datetime(
            news_dataframe['pubDate']).dt.strftime('%Y%m%d')
        news_dataframe = news_dataframe.join(publish_dates,
                                             rsuffix='_formatted')
        # Convert the DataFrame into a csv file
        with open(os.path.join('docs', 'requested_news_storage.csv'), 'a',
                  encoding='utf-16') as log_file:
            news_dataframe.to_csv(log_file, sep=';', header=False,
                                  index=False, encoding='utf-16')


class CachedNewsReader(NewsReader):
    """
    A class used to represent a RSS container for the news items retrieved
    from the local storage.

    Attributes
    ----------
    feed : str
        the title of the rss feed
    publish_date : str
        the date the news published on are to be found in the local storage
    items : list
        the list of RSSItem instances
    items_limit : int
        the number of items to yield from iterator object
    """

    @rss_logger(logger)
    def __init__(self, rss_url, publish_date, items_limit=None):
        """
        Construct an instance of CachedNewsReader class and set values for
        feed, publish_date, items and items_limit attributes.
        :param rss_url: str
        The URL string news from the which are to be found in the local storage
        :param publish_date: int
        The date the news published on are to be found in the local storage
        :param items_limit: int
        The number of items to yield from iterator object (default is None)
        """
        NewsReader.__init__(self, rss_url, items_limit)
        self.feed = ''
        self.publish_date = publish_date
        self.items = self.__set_items()
        self.items_limit = (
            items_limit if items_limit and items_limit < len(
                self.items) else len(self.items))

    @rss_logger(logger)
    def __set_items(self):
        """
        Generate a list of RSSItem instances.

        :raise DateNotValidError
        If no cached news published on the specified date are found
        :raise NoCachedRSSFeedFoundError
        If no cached news from the specified feed are found
        :return: list
        The list of RSSItem instances
        """
        rss_items = []
        # Read items from the csv file (local storage)
        cached_news = pd.read_csv(
            os.path.join('docs', 'requested_news_storage.csv'),
            sep=';',
            decimal=',',
            header=None,
            names=['feed', 'feed_url', 'title', 'pubDate', 'link',
                   'description_text', 'description_links',
                   'description_images', 'pubDate_formatted'],
            usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            parse_dates=['pubDate_formatted'],
            infer_datetime_format=True,
            skip_blank_lines=True,
            encoding='utf-16')
        # Remove possible duplicates
        cached_news.drop_duplicates(inplace=True)

        try:
            # Pick up the news by the date
            selected_by_date_news = cached_news.loc[
                cached_news['pubDate_formatted'] == self.publish_date]
            # If DataFrame is empty raise DateNotValidError
            if selected_by_date_news.empty:
                raise DateNotValidError('There are no cached news published '
                                        'on the specified date. Please, try '
                                        'another date.')
            # Pick up the news by the feed
            if self.url:
                selected_by_date_and_feed_news = selected_by_date_news.loc[
                    selected_by_date_news['feed_url'] == self.url]
                # If DataFrame is empty raise NoCachedRSSFeedFoundError
                if selected_by_date_and_feed_news.empty:
                    raise NoCachedRSSFeedFoundError(
                        'There are no cached news from the specified feed. '
                        'Please, try another URL.')
                self.feed = selected_by_date_and_feed_news.iat[0, 0]
                # Set a list of JSON formatted news items from the DataFrame
                selected_news_json = selected_by_date_and_feed_news.to_json(
                    orient='records', force_ascii=False)
            else:
                selected_news_json = selected_by_date_news.to_json(
                    orient='records', force_ascii=False)
            # Get list of dictionaries for each news item
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
                            RSSItemDescription(text=description_text,
                                               links=description_links,
                                               images=description_images)))
        except DateNotValidError as error:
            print(error)
        except NoCachedRSSFeedFoundError as error:
            print(error)
        finally:
            return rss_items


class RSSItem:
    """
    A class used to represent a RSSItem container for the parsed
    structure of a RSS channel item.

    Attributes
    ----------
    feed : str
        the item's parent RSS feed title
    feed_url : str
        the item's parent RSS feed URL
    title : str
        the item's headline
    publish_date : str
        the publication date and time of the item
    link : str
        the URL of a web page associated with the item
    description : RSSItemDescription
        the RSSItemDescription instance (default is None)
    json : JSON formatted str
        the item presented by a JSON formatted str
    """

    @rss_logger(logger)
    def __init__(self, feed, feed_url, title=None, publish_date=None,
                 link=None, description=None):
        """
        Construct an instance of RSSItem class and set values for feed,
        feed_url and json attributes.

        :param feed: str
        The item's parent RSS feed title
        :param feed_url: str
        The item's parent RSS feed URL
        :param title: str
        The item's headline (default is None)
        :param publish_date: str
        The publication date and time of the item (default is None)
        :param link: str
        The URL of a web page associated with the item (default is None)
        :param description: RSSItemDescription
        The RSSItemDescription instance (default is None)
        """
        self.feed = feed
        self.feed_url = feed_url
        self.__set_title(title)
        self.__set_publish_date(publish_date)
        self.__set_link(link)
        self.__set_description(description)
        self.json = self.__generate_json()

    @rss_logger(logger)
    def __set_title(self, title):
        """
        Set value for title attribute.

        :param title: str
        The item's headline
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
        Set value for publish_date attribute.

        :param publish_date: str
        The publication date and time of the item
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
        Set value for link attribute.

        :param link: str
        The URL of a web page associated with the item
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
        Set value for description attribute.

        :param description: RSSItemDescription
        The RSSItemDescription instance
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
                    "description_text": (
                        None if self.description is None
                        else self.description.description_text
                    ),
                    "description_links": (
                        None if self.description is None
                        else self.description.description_links
                    ),
                    "description_images": (
                        None if self.description is None
                        else self.description.description_images
                    )
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

    @rss_logger(logger)
    def __init__(self, *, description=None, text=None,
                 links=None, images=None):
        """
        Construct an instance of RSSItemDescription class.

        :param description: str
        The HTML text of the description part of the RSS channel item
        (default is None)
        :param text: str
        The text of the description part of the RSS channel item
        :param links: str
        The string containing the URLs from the description part of the RSS
        channel item
        :param images: str
        The string containing the URLs to the images from the description
        part of the RSS channel item
        """
        self.__set_description(description=description, text=text,
                               links=links, images=images)
        self.__set_extension()

    @rss_logger(logger)
    def __set_description(self, **kwargs):
        """
        Set values for description_text, description_links and
        description_images attributes.

        :param **kwargs: dict
        The dictionary containing
             description: str
             The HTML text of the description part of the RSS channel item
             text: str
             The text of the description part of the RSS channel item
             links: str
             The string containing the URLs from the description part of
             the RSS channel item
             images: str
             The string containing the URLs to the images from the
             description part of the RSS channel item
        """
        if kwargs['description'] is not None:
            # Parse the text data and URLs from the HTML text of the
            # description part of the RSS channel item
            description_parser = DescriptionHTMLParser()
            description_parser.feed(kwargs['description'].text)
            # Set the text data parsed from HTML text of the rss channel item
            # description
            self.description_text = description_parser.parsed_text_data
            # Set the list of URLs met in the rss channel item description
            self.description_links = list(description_parser.parsed_links)
            # Set the list of URLs to images met in the rss channel item
            # description
            self.description_images = list(description_parser.parsed_images)
        else:
            self.description_text = kwargs['text'] if kwargs['text'] else ''
            # If the list of links is not empty
            if kwargs['links']:
                # Remove extra quotes
                self.description_links = [
                    link.strip("'\"")
                    for link
                    in kwargs['links'].strip('[]').split(', ')
                ]
            else:
                self.description_links = []
            # If the list of images is not empty
            if kwargs['images']:
                # Remove extra quotes
                self.description_images = [
                    image.strip("'\"")
                    for image
                    in kwargs['images'].strip('[]').split(', ')
                ]
            else:
                self.description_images = []

    @rss_logger(logger)
    def __set_extension(self):
        """
        Set a value for description_extension attribute.

        """
        # Compiled the string with the text for printing out in stdout from
        # description_links and description_images.
        if self.description_links or self.description_images:
            # Begin with the 'Links:'
            description_extension = 'Links:\n'
            line_number = 1
            # Add a new line for each link
            for link in self.description_links:
                new_line = '[' + str(line_number) + ']: ' + link + ' (link)\n'
                description_extension += new_line
                line_number += 1
            # Add a new line for each link
            for image in self.description_images:
                new_line = ('[' + str(line_number) + ']: ' + image
                            + ' (image)\n')
                description_extension += new_line
                line_number += 1
        else:
            description_extension = ''
        # Set the value for description_extension attribute
        self.description_extension = description_extension
