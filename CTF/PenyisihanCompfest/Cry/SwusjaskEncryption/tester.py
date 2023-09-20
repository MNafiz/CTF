import random
from Crypto.Util.number import *

p = 1179478847235411356076287763101027881
# p = 17

def square_root(a, p):
    #Tonelli–Shanks algorithm
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) / 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a, p):

    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

class MultiplicativeGroup:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(self, other) -> "MultiplicativeGroup":
        a = (self.a * other.a - 6969 * self.b * other.b) % p
        b = (self.a * other.b + self.b * other.a - 69 * self.b * other.b) % p
        return MultiplicativeGroup(a, b)

    def __pow__(self, n) -> "MultiplicativeGroup":
        res = MultiplicativeGroup(1, 0)
        base = self
        while n:
            if n & 1:
                res *= base
            base *= base
            n >>= 1
        return res
    
    def __repr__(self):
        return f"({self.a}, {self.b})"

def bytes_to_block(msg: bytes):
    res = []
    msg_int = bytes_to_long(msg)
    print("udah")
    while msg_int:
        print(msg_int)
        res.append(msg_int % (p**2))
        msg_int //= p**2
    return res


def block_to_bytes(blocks):
    res = 0
    for i in range(len(blocks) - 1, -1, -1):
        res *= p**2
        res += blocks[i]
    return long_to_bytes(res)

m = MultiplicativeGroup(1,2)

e = 0x10001
d = inverse(e, p ** 2 - 1)
print(m ** (e * d))

FLAG = open("flag.enc", "rb").read()
blocks = bytes_to_block(FLAG)
