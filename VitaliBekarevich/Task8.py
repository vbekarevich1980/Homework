# Task 6.8
#
# Implement a Pagination class helpful to arrange text on pages and list content on given page.
# The class should take in a text and a positive integer which indicate how many symbols will be allowed per each page
# (take spaces into account as well).
# You need to be able to get the amount of whole symbols in text, get a number of pages that came out and method that
# accepts the page number and return quantity of symbols on this page.
# If the provided number of the page is missing print the warning message "Invalid index. Page is missing". If you're
# familiar with using of Exceptions in Python display the error message in this way.
# Pages indexing starts with 0.
#
# Example:
# ```python
# >>> pages = Pagination('Your beautiful text', 5)
# >>> pages.page_count
# 4
# >>> pages.item_count
# 19
#
# >>> pages.count_items_on_page(0)
# 5
# >>> pages.count_items_on_page(3)
# 4
# >>> pages.count_items_on_page(4)
# Exception: Invalid index. Page is missing.
# ```
# Optional: implement searching/filtering pages by symbols/words and displaying pages with all the symbols on it.
# If you're querying by symbol that appears on many pages or if you are querying by the word that is split in two
# return an array of all the occurrences.
#
# Example:
# ```python
# >>> pages.find_page('Your')
# [0]
# >>> pages.find_page('e')
# [1, 3]
# >>> pages.find_page('beautiful')
# [1, 2]
# >>> pages.find_page('great')
# Exception: 'great' is missing on the pages
# >>> pages.display_page(0)
# 'Your '
# ```
from math import ceil


class Pagination:
    def __init__(self, text, symbols_per_page):
        self.text = text
        self.symbols_per_page = symbols_per_page
        self.page_count = ceil(len(text) / symbols_per_page)
        self.item_count = len(text)

    def count_items_on_page(self, page_number):
        if page_number == self.page_count - 1:
            return self.item_count % self.symbols_per_page
        elif page_number >= self.page_count:
            raise Exception('Invalid index. Page is missing')
        else:
            return self.symbols_per_page

    def find_page(self, search_text):
        search_text_positions = [i for i in range(self.item_count) if self.text.startswith(search_text, i)]
        res = []
        for position in search_text_positions:
            for i in range(0, self.item_count, self.symbols_per_page):
                if (i <= position < i + self.symbols_per_page
                        or i <= position + len(search_text) < i + self.symbols_per_page):
                    res.append(i // self.symbols_per_page)
        if res:
            return res
        else:
            raise Exception(f"'{search_text}' is missing on the pages")

    def display_page(self, page_number):
        if page_number < self.page_count:
            return self.text[page_number * self.symbols_per_page:(page_number + 1) * self.symbols_per_page]
        else:
            raise Exception('Invalid index. Page is missing')


pages = Pagination('Your beautiful text', 5)
print(pages.page_count)
print(pages.item_count)
print(pages.count_items_on_page(0))
print(pages.count_items_on_page(3))
# print(pages.count_items_on_page(4))
print(pages.find_page('Your'))
print(pages.find_page('e'))
print(pages.find_page('beautiful'))
# print(pages.find_page('great'))
print(pages.display_page(0))
print(pages.display_page(2))
