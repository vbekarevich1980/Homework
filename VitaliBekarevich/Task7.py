# Task 6.7
# Implement a class Money to represent value and currency.
# You need to implement methods to use all basic arithmetics expressions (comparison, division, multiplication,
# addition and subtraction).
# Tip: use class attribute exchange rate which is dictionary and stores information about exchange rates to your
# default currency:
# ```python
# exchange_rate = {
#     "EUR": 0.93,
#     "BYN": 2.1,
#     ...
# }
# ```
#
# Example:
# ```python
# x = Money(10, "BYN")
# y = Money(11) # define your own default value, e.g. “USD”
# z = Money(12.34, "EUR")
# print(z + 3.11 * x + y * 0.8) # result in “EUR”
# >>543.21 EUR
#
# lst = [Money(10,"BYN"), Money(11), Money(12.01, "JPY")]
# s = sum(lst)
# print(s) #result in “BYN”
# >>123.45 BYN
# ```
#
# <em>Have a look at @functools.total_ordering</em>

from functools import total_ordering


@total_ordering
class Money:
    exchange_rate = {
        'EUR': 0.856,
        'USD': 1,
        'BYN': 2.5,
        'JPY': 111.3055,
        'RUB': 72.5783,
        'UAN': 26.5808,
        'PLN': 3.9543,
    }

    def __init__(self, value, currency='USD'):
        self.value = value
        self.currency = currency

    def __str__(self):
        return f'{self.value:.2f} {self.currency}'

    def __repr__(self):
        return f'{self.value:.2f} {self.currency}'

    def __add__(self, other):  # x + 1
        return (Money(self.value + other.value / Money.exchange_rate[other.currency]
                      * Money.exchange_rate[self.currency], self.currency))

    def __radd__(self, other):  # 1 + x
        if other == 0:
            return Money(self.value, self.currency)
        else:
            return (Money(other.value + self.value / Money.exchange_rate[self.currency]
                          * Money.exchange_rate[other.currency], other.currency))

    def __iadd__(self, other):  # x += 1
        return (Money(self.value + other.value / Money.exchange_rate[other.currency]
                      * Money.exchange_rate[self.currency], self.currency))

    def __eq__(self, other):  # x == 1
        return (round(self.value / Money.exchange_rate[self.currency], 2)
                == round(other.value / Money.exchange_rate[other.currency], 2))

    def __lt__(self, other):  # x < 1
        return (round(self.value / Money.exchange_rate[self.currency], 2)
                < round(other.value / Money.exchange_rate[other.currency], 2))

    def __divmod__(self, other):  # x % 1, x // 1
        return Money(self.value // other, self.currency), Money(self.value % other, self.currency)

    def __rdivmod__(self, other):  # 1 % x, 1 // x
        return f"Операция недопустима."

    def __truediv__(self, other):  # x / 1
        return Money(self.value / other, self.currency)

    def __rtruediv__(self, other):  # 1 / x
        return f"Операция '{other} / {self}' недопустима."

    def __itruediv__(self, other):  # x /= 1
        return Money(self.value / other, self.currency)

    def __floordiv__(self, other):  # x // 1
        return Money(self.value // other, self.currency)

    def __rfloordiv__(self, other):  # 1 // x
        return f"Операция '{other} // {self}' недопустима."

    def __ifloordiv__(self, other):  # x //= 1
        return Money(self.value // other, self.currency)

    def __mod__(self, other):  # x % 1
        return Money(self.value % other, self.currency)

    def __rmod__(self, other):  # 1 % x
        return f"Операция '{other} % {self}' недопустима."

    def __imod__(self, other):  # x %= 1
        return Money(self.value % other, self.currency)

    def __mul__(self, other):  # x * 1
        return Money(self.value * other, self.currency)

    def __rmul__(self, other):  # 1 * x
        return Money(self.value * other, self.currency)

    def __imul__(self, other):  # x *= 1
        return Money(self.value * other, self.currency)

    def __sub__(self, other):  # x - 1
        return (Money(self.value - other.value / Money.exchange_rate[other.currency]
                      * Money.exchange_rate[self.currency], self.currency))

    def __rsub__(self, other):  # 1 - x
        return (Money(other.value - self.value / Money.exchange_rate[self.currency]
                      * Money.exchange_rate[other.currency], other.currency))

    def __isub__(self, other):  # x -= 1
        return (Money(self.value - other.value / Money.exchange_rate[other.currency]
                      * Money.exchange_rate[self.currency], self.currency))


x = Money(10, "BYN")
y = Money(11)  # define your own default value, e.g. “USD”
z = Money(12.34, "EUR")
v = Money(3.43, "EUR")
print(z + 3.11 * x + y * 0.8)  # result in “EUR”
lst = [Money(10, "BYN"), Money(11), Money(12.01, "JPY")]
print(lst)
s = sum(lst)
print(s)  # result in “BYN”
print(x)
print(v)
print(x == v)
print(x < v)
print(x > v)
print(x <= v)
print(x != v)
print(x + y)
print(y - x)
print(y + x + v)
print(x - y)
x -= y
print(x)
print(x + y)
print(y / 3)
print(3 / y)
print(y // 3)
print(3 // y)
print(y % 3)
print(3 % y)
print(y * 3)
print(3 * y)
print(divmod(y, 3))
