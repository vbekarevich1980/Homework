# Task 6.2
# Implement custom dictionary that will memorize 10 latest changed keys.
# Using method "get_history" return this keys.
#
# Example:
# ```python
# >>> d = HistoryDict({"foo": 42})
# >>> d.set_value("bar", 43)
# >>> d.get_history()
#
# ["bar"]
# ```
#
# <em>After your own implementation of the class have a look at collections.deque
# https://docs.python.org/3/library/collections.html#collections.deque </em>


class HistoryDict:
    def __init__(self, a_dict):
        self._dict = a_dict
        self.history = []

    def set_value(self, key, value):
        self._dict[key] = value
        if key in self.history:
            self.history.remove(key)
        if len(self.history) >= 10:
            self.history.pop(0)
        self.history.append(key)

    def get_history(self):
        return self.history


d = HistoryDict({"foo": 42})
d.set_value("bar", 43)
d.set_value("top", 45)
d.set_value("bar", 43)
d.set_value("bar1", 43)
d.set_value("bar2", 43)
d.set_value("bar3", 43)
d.set_value("bar4", 43)
d.set_value("bar5", 43)
d.set_value("bar6", 43)
d.set_value("bar7", 43)
d.set_value("bar8", 43)
d.set_value("bar9", 43)
d.set_value("top", 45)

print(d.get_history())
