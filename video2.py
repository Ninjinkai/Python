#!/usr/bin/python

import math, decimal

# Demo integers

x, y, z = 1, 2, 3

print(x, y, z)

def boolEx(a, b):
    print("a:", a, type(a))
    print("b:", b, type(b))
    print("a and b:", a and b)
    print("a or b:", a or b)
    print("not a, not b:", not a, not b)

boolEx(True, False)

print("{} * {} + {} =".format(x, y, z), x*y+z)

print("13 =", bin(13))
print("-13 =", bin(-13))

print(math.ceil(y/z))
print(math.gcd(120,45))
