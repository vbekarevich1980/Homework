#!/usr/bin/python

import argparse
from rss_reader import config, my_rss


parser = argparse.ArgumentParser(
    description='Pure Python command-line RSS reader.')
parser.add_argument('source',
                    help='RSS URL')
parser.add_argument('--version', action='version',
                    version='%(prog)s ' + config.version,
                    help='Print version info')
parser.add_argument('--json', action='store_true',
                    help='Print result as JSON in stdout')
parser.add_argument('--verbose', action='store_true',
                    # TODO можно задать count и default = 0 1 раз - просто что
                    #  делаю
                    # сейчас, 2 раза детальнее should print logs in the process
                    # of application running, not after
                    # everything is done.
                    help='Outputs verbose status messages')
parser.add_argument('--limit', type=int,
                    help='Limit news topics if this parameter provided')

args = parser.parse_args()


rss = my_rss.RSS(args.source, args.limit)
print('-' * 50)
print('Feed:', rss.title)
print('-' * 50)

if args.json:
    for item in rss:
        print(item.json)
        print('-' * 20)
else:
    for item in rss:
        if item.title is not None:
            print('Title:', item.title)  # TODO check if there are any items
        if item.link is not None:
            print('Link:', item.link)
        if item.publish_date is not None:
            print('Date:', item.publish_date, '\n')
        if item.description is not None:
            print(item.description.description_text, '\n')
        if item.description is not None:
            print(item.description.description_extension)
        print('-' * 20)
