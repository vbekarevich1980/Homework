# Task 6.1
# Implement a Counter class which optionally accepts the start value and the counter stop value.
# If the start value is not specified the counter should begin with 0.
# If the stop value is not specified it should be counting up infinitely.
# If the counter reaches the stop value, print "Maximal value is reached."
#
# Implement two methods: "increment" and "get"
#
# * <em>If you are familiar with Exception rising use it to display the "Maximal value is reached." message.</em>
#
# Example:
# ```python
# >>> c = Counter(start=42)
# >>> c.increment()
# >>> c.get()
# 43
#
# >>> c = Counter()
# >>> c.increment()
# >>> c.get()
# 1
# >>> c.increment()
# >>> c.get()
# 2
#
# >>> c = Counter(start=42, stop=43)
# >>> c.increment()
# >>> c.get()
# 43
# >>> c.increment()
# Maximal value is reached.
# >>> c.get()
# 43
# ```

class Counter:
    def __init__(self, start=0, stop=None):
        self.value = start
        self.stop = stop

    def increment(self):
        if self.stop is None or self.value < self.stop:
            self.value += 1
        else:
            raise Exception('Maximal value is reached.')

    def get(self):
        return self.value


c = Counter(start=42)
c.increment()
c.increment()
c.increment()
c.increment()
c.increment()
c.increment()
c.increment()
c.increment()

print(c.get())

c = Counter()
c.increment()
print(c.get())

c.increment()
print(c.get())

c = Counter(start=42, stop=43)
c.increment()
print(c.get())

c.increment()
print(c.get())
