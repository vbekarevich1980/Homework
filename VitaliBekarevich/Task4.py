# Task 6.4
# Create hierarchy out of birds.
# Implement 4 classes:
# * class `Bird` with an attribute `name` and methods `fly` and `walk`.
# * class `FlyingBird` with attributes `name`, `ration`, and with the same methods. `ration` must have default value.
# Implement the method `eat` which will describe its typical ration.
# * class `NonFlyingBird` with same characteristics but which obviously without attribute `fly`.
# Add same "eat" method but with other implementation regarding the swimming bird tastes.
# * class `SuperBird` which can do all of it: walk, fly, swim and eat.
# But be careful which "eat" method you inherit.
#
# Implement str() function call for each class.
#
# Example:
# ```python
# >>> b = Bird("Any")
# >>> b.walk()
# "Any bird can walk"
#
# p = NonFlyingBird("Penguin", "fish")
# >> p.swim()
# "Penguin bird can swim"
# >>> p.fly()
# AttributeError: 'Penguin' object has no attribute 'fly'
# >>> p.eat()
# "It eats mostly fish"

# c = FlyingBird("Canary")
# >>> str(c)
# "Canary can walk and fly"
# >>> c.eat()
# "It eats mostly grains"
#
# s = SuperBird("Gull")
# >>> str(s)
# "Gull bird can walk, swim and fly"
# >>> s.eat()
# "It eats fish"
# ```
#
# Have a look at __mro__ method of your last class.

class Bird:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name} bird can walk and fly'

    def fly(self):
        return f'{self.name} bird can fly'

    def walk(self):
        return f'{self.name} bird can walk'


class FlyingBird(Bird):
    def __init__(self, name, ration='grains'):
        Bird.__init__(self, name)
        self.ration = ration

    def eat(self):
        return f'It eats mostly {self.ration}'


class NonFlyingBird(Bird):
    def __init__(self, name, ration='fish'):
        Bird.__init__(self, name)
        self.ration = ration

    def __str__(self):
        return f'{self.name} bird can walk and swim'

    def eat(self):
        return f'It eats mostly {self.ration}'

    def __getattribute__(self, item):
        if item == 'fly':
            raise AttributeError(f"'{self.name}' object has no attribute 'fly'")
        else:
            return Bird.__getattribute__(self, item)

    def swim(self):
        return f'{self.name} bird can swim'


class SuperBird(NonFlyingBird, FlyingBird):
    def __str__(self):
        return f'{self.name} bird can walk, swim and fly'

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)


b = Bird("Any")
print(str(b))
print(b.walk())
print(b.fly())
# print(b.swim())
# print(b.eat())

p = NonFlyingBird("Penguin", "fish")
print(str(p))
print(p.walk())
print(p.swim())
# print(p.fly())
print(p.eat())

c = FlyingBird("Canary")
print(str(c))
print(c.walk())
# print(c.swim())
print(c.fly())
print(c.eat())

s = SuperBird("Gull")
print(str(s))
print(s.walk())
print(s.swim())
print(s.fly())
print(s.eat())

print(SuperBird.mro())
