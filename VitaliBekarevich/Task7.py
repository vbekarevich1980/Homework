# Task 5.7*
"""
# Run the module `modules/mod_a.py`. Check its result. Explain why does this happen.

Result = '5'.
Buy running mod_a we
 1) import mod_c, code of mod_c runs and creates variable x = 5.
 2) import mod_b, code of mod_b runs and do 1), and after that overwrites variable x of mod_c with 5
 3) we print variable of mod_c out


# Try to change x to a list `[1,2,3]`. Explain the result.

We have changed x in mod_c with `[1,2,3]`. Result = '5'.
Buy running mod_a we
 1) import mod_c, code of mod_c runs and creates variable x = [1,2,3].
 2) import mod_b, code of mod_b runs and do 1), and after that overwrites variable x of mod_c with 5
 3) we print variable of mod_c out


# Try to change import to `from x import *` where x - module names. Explain the result.

from mod_c import *
from mod_b import *

print(x)
print(mod_c.x)

result:
[1, 2, 3]
5

Buy running mod_a we
 1) from mod_c import * creates a copy of its variable x = [1,2,3] and it becomes variable of mod_a
 2) from mod_b import * import a copy of variable 'mod_c', which was created in mod_b by running the code of
 mod_c (import mod_c). Variable 'mod_c' is connected with the object of mod_c.py and let us access its
 variable x in mod_c, which was overwritten with 5 inside mod_b
 3) we print variable of mod_c out
"""
