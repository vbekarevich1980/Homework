# Task 6.6
# A singleton is a class that allows only a single instance of itself to be created and gives access to that created
# instance.
# Implement singleton logic inside your custom class using a method to initialize class instance.
# Example:
#
# ```python
# >>> p = Sun.inst()
# >>> f = Sun.inst()
# >>> p is f
# True
# ```

class Sun:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sun, cls).__new__(cls)
        return cls.instance

    def __init__(self, name='Singleton'):
        self.name = name

    def inst(self):
        if not hasattr(self.__class__, 'instance'):
            return Sun()
        else:
            return Sun.instance


p = Sun().inst()
f = Sun().inst()
g = Sun()
h = Sun()

print(p is f)
print(f is g)
print(g is h)
print(p)
print(f)
print(g)
print(h)
print(p.name)
print(f.name)
print(g.name)
print(h.name)
