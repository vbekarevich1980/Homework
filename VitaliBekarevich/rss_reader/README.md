# Pure Python command-line RSS reader.

This script allows the user to print to the console all news from the RSS
found in the URL passed to the utility. It is assumed that the URL leads
to a RSS feed. It allows saves the retrieved news to the local storage and
allows the user to get them later filtered on the specified date, it also
allows to convert the news into pdf and html format.

This tool accepts a string with a URL and some optional arguments to
specify the print out.

```
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
```
# Local storage

The news items are stored locally in the docs directory. For storing the news 
Pandas DataFrame is used which is then saved into .csv file 
requested_news_storage.csv.
The structure uses the structure of JSON used in the utility (see JSON.md), 
i.e. it has the following columns:
    "feed": str -- "RSS feed channel title"
    "feed_url": str -- "RSS feed URL"
    "title": str -- "News item title"
    "pubDate": str -- "News publishing date"
    "link": str -- "News item URL"
    "description_text": str -- "News item text"
    "description_links": list of strings -- "News item additional URLs"
    "description_images": list of strings -- "News item images URLs"
Plus another column with dates of news publishing in datetime format is added.

# PDF converter

The news items are converted into PDF format with reportlab package. For 
cyrillic Times.tcc is used sitting in the docs directory.
