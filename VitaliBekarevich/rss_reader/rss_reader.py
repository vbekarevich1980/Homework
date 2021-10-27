#!/usr/bin/python
"""
Pure Python command-line RSS reader.

This script allows the user to print to the console all news from the RSS
found in the URL passed to the utility. It is assumed that the URL leads
to a RSS feed.

This tool accepts a string with a URL and some optional arguments to
specify the print out.

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     source
positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

This file contains the following functions:

    * def news_printer - prints into stdout the title of the RSS feed and
    the news items below
    * main - the main function of the script
"""

import argparse
import logging
import logging.config
from rss_reader_p import config, rss


def news_printer(args):
    """
    Print into stdout the title of the rss feed and the news items below.

    :param args: argparse.Namespace
    The arguments intercepted by argparse from command line
    """
    rss_feed = rss.RSS(args.source, args.limit)
    print('-' * 50)
    print('Feed:', rss_feed.title)
    print('-' * 50)

    if args.json:
        for item in rss_feed:
            print(item.json)
            print('-' * 20)
    else:
        for item in rss_feed:
            if item.title is not None:
                print('Title:',
                      item.title)  # TODO check if there are any  # items
            if item.link is not None:
                print('Link:', item.link)
            if item.publish_date is not None:
                print('Date:', item.publish_date, '\n')
            if item.description is not None:
                print(item.description.description_text, '\n')
            if item.description is not None:
                print(item.description.description_extension)
            print('-' * 20)


    rss_feed.cash_news_items()


def main():
    """
    The main function.

    """
    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL', nargs='?', default='')  # TODO nargs='?', default=''
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + config.version,
                        help='Print version info')
    parser.add_argument('--json', action='store_true',
                        help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int,
                        help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=str,
                        help='Print the cached news published on the specified'
                             ' date. The date should be provided in YYYYMMDD '
                             'format')

    args = parser.parse_args()

    if args.verbose:
        config.log_config['loggers']['rss_reader']['level'] = 'DEBUG'

    logging.config.dictConfig(config.log_config)
    #logger = logging.getLogger('rss_reader')

    #news_printer(args)
    if args.date:
        rss_feed = rss.LocalStorage(args.source, args.date, args.limit)

    else: # TODO отловить ошибку если нет источника и нет даты
        rss_feed = rss.RSS(args.source, args.limit)
        rss_feed.cash_news_items()
    if args.json:
        rss_feed.json_to_console_printer()
    else:
        rss_feed.news_to_console_printer()

    rss_feed.news_to_pdf_converter()
    rss_feed.news_to_html_converter()








if __name__ == '__main__':
    main()
