#!/usr/bin/python
"""
Pure Python command-line RSS reader.

This script allows the user to print to the console all news from the RSS
found in the URL passed to the utility. It is assumed that the URL leads
to a RSS feed. It allows saves the retrieved news to the local storage and
allows the user to get them later filtered on the specified date, it also
allows to convert the news into pdf and html format.

This tool accepts a string with a URL and some optional arguments to
specify the print out.

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                     [--date YYYYMMDD] [--to-pdf PATH] [--to-html PATH]
                     [source]
positional arguments:
  source         RSS URL

optional arguments:
  -h, --help       show this help message and exit
  --version        Print version info
  --json           Print result as JSON in stdout
  --verbose        Outputs verbose status messages
  --limit LIMIT    Limit news topics if this parameter provided
  --date YYYYMMDD  Print the cached news published on the specified date.
                   The date should be provided in YYYYMMDD format
  --to-pdf PATH    Convert the news into pdf format and stores the pdf
                   file to the specified location
  --to-html PATH   Convert the news into html format and stores the html
                   file to the specified location

This file contains the following functions:

    * main - the main function of the script
"""

import argparse
import logging
import logging.config
from rss_reader_p import config


def main():
    """
    The main function.

    """
    # Initiate an ArgumentParser instance with needed arguments
    parser = argparse.ArgumentParser(
        description='Pure Python command-line RSS reader.')
    parser.add_argument('source', help='RSS URL', nargs='?', default='')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + config.version,
                        help='Print version info')
    parser.add_argument('--json', action='store_true',
                        help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int,
                        help='Limit news topics if this parameter provided')
    parser.add_argument('--date', metavar='YYYYMMDD', type=str,
                        help='Print the cached news published on the specified'
                             ' date. The date should be provided in YYYYMMDD '
                             'format')
    parser.add_argument('--to-pdf', metavar='PATH', type=str,
                        help='Convert the news into pdf format and stores the '
                             'pdf file to the specified location')
    parser.add_argument('--to-html', metavar='PATH', type=str,
                        help='Convert the news into html format and stores the'
                             ' html file to the specified location')

    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        config.log_config['loggers']['rss_reader_p']['level'] = 'DEBUG'

    logging.config.dictConfig(config.log_config)

    from rss_reader_p import rss

    # Create the main logic of the script depending on the parsed arguments
    if args.date:
        reader = rss.CachedNewsReader(args.source, args.date, args.limit)
    else:
        reader = rss.RSSNewsReader(args.source, args.limit)
        reader.cash_news_items()
    if args.json:
        reader.json_to_console_printer()
    if args.to_pdf:
        reader.news_to_pdf_converter(args.to_pdf, args.date)
    elif args.to_html:
        reader.news_to_html_converter(args.to_html, args.date)
    elif not args.json:
        reader.news_to_console_printer()


if __name__ == '__main__':
    main()
