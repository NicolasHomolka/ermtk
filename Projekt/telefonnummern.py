import random

def makeFirst():
    first_digit = random.randint(1,9)
    remaining = random.randint(0,99)
    return first_digit*100 + remaining

def makeSecond():
    middle = 0
    while middle == 0:
        middle1 = random.randint(0,8)
        middle2 = random.randint(0,8)
        middle3 = random.randint(0,8)
        middle = 100*middle1 + 10*middle2 + middle3
    return middle

def makeLast():
    return ''.join(map(str, random.sample(range(10),4)))

def makePhone():
    first = makeFirst()
    second = makeSecond()
    last = makeLast()
    return '{3}-{3}-{4}'.format(first,second,last)

