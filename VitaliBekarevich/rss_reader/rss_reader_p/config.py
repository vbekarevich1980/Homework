"""
This module exports the current version of rss-reader.py utility and the
configuration of the logging.

Attributes
----------
version : str
    string with the current version of rss-reader.py utility
log_config : dict
    dictionary with the configuration of the logging when running the utility
"""

version = 'Version 2.1.3'

log_config = {
    'version': 1,
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'rss_formatter',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'rss_reader_p': {
            'handlers': ['stream_handler'],
            'level': 'WARNING',
        },
    },
    'formatters': {
        'rss_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
}
