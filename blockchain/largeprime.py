import random
import math

def is_probably_prime(n, k=5):
    if n < 2:
        return False
    for _ in range(k):
        a = random.randint(2, n-1)
        x = pow(a, n-1, n)
        if x != 1:
            return False
    return True

def generate_large_prime(bit_length):
    while True:
        n = random.getrandbits(bit_length)
        if is_probably_prime(n):
            return n

def gcd(a, b):
    """Returns the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def is_primitive_root(g, p):
    """Returns True if g is a primitive root modulo p, False otherwise."""
    phi = p-1
    factors = []
    d = 2
    while d*d <= phi:
        if phi % d == 0:
            factors.append(d)
            while phi % d == 0:
                phi //= d
        d += 1
    if phi > 1:
        factors.append(phi)
    for factor in factors:
        if pow(g, (p-1)//factor, p) == 1:
            return False
    return True

def find_generator(p):
    """Finds a generator of the prime number p."""
    while True:
        g = random.randint(2, p-1)
        if gcd(g, p) == 1 and is_primitive_root(g, p):
            return g


def toret():
    x = generate_large_prime(20)
    print(x)
    print(find_generator(x))
    return find_generator(x)

def is_probably_prime(n, k=5):
    if n < 2:
        return False
    for _ in range(k):
        a = random.randint(2, n-1)
        x = pow(a, n-1, n)
        if x != 1:
            return False
    return True

def generate_large_prime(bit_length):
    while True:
        n = random.getrandbits(bit_length)
        if is_probably_prime(n):
            return n

def gcd(a, b):
    """Returns the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def is_primitive_root(g, p):
    """Returns True if g is a primitive root modulo p, False otherwise."""
    phi = p-1
    factors = []
    d = 2
    while d*d <= phi:
        if phi % d == 0:
            factors.append(d)
            while phi % d == 0:
                phi //= d
        d += 1
    if phi > 1:
        factors.append(phi)
    for factor in factors:
        if pow(g, (p-1)//factor, p) == 1:
            return False
    return True

def find_generator(p):
    """Finds a generator of the prime number p."""
    while True:
        g = random.randint(2, p-1)
        if gcd(g, p) == 1 and is_primitive_root(g, p):
            return g


def toret():
    x = generate_large_prime(20)
    print(x)
    print(find_generator(x))
    return find_generator(x)
    
if __name__ == '__main__':
    toret()
    
