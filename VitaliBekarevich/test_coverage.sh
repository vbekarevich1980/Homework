coverage erase
coverage run --source=./rss_reader -m unittest discover ./tests
coverage report -m
coverage html
open ./htmlcov/index.html