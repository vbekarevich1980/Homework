"""
This module exports DescriptionHTMLParser class presenting a tool for
parsing HTML text of the rss channel item description.

class DescriptionHTMLParser -- the class for parsing HTML text of
the rss channel item description
"""

from html.parser import HTMLParser


class DescriptionHTMLParser(HTMLParser):
    """
    A class used to represent a DescriptionHTMLParser parser of the HTML
    text of the rss channel item description.

    Attributes
    ----------
    parsed_links : set
        the set of URLs met in the rss channel item description
    parsed_images : set
        the set of URLs to images met in the rss channel item description
    parsed_text_data : str
        the text data parsed from HTML text of the rss channel item
        description
    """

    def error(self, message):
        """
        Intercept the unexpected error and print the error message to stdout.

        :param message: str
        """
        print('Unexpected error has occurred:', message)

    def __init__(self):
        """
        Override __init__ of the superclass HTMLParser to construct an
        instance of DescriptionHTMLParser class and set values for
        parsed_links, parsed_images, parsed_text_data attributes.

        """
        super().__init__()
        self.parsed_links = set()
        self.parsed_images = set()
        self.parsed_text_data = ''

    def handle_starttag(self, tag, attrs):
        """
        Handle the start of a tag (e.g. <a href="https://...">) to
        retrieve URLs from the tag attributes.

        :param tag: str
        The name of the tag converted to lower case
        :param attrs: list
        The list of (name, value) pairs containing the attributes found
        inside the tag’s <> brackets
        """
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.parsed_links.add(attr[1])
        elif tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.parsed_images.add(attr[1])

    def handle_data(self, data):
        """
        Process arbitrary data of the HTML text to retrieve the text
        of the description.

        :param data: str
        The text data inside HTML string
        """
        self.parsed_text_data += data
