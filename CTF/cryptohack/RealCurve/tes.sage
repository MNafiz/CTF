from sage.all import *
from Crypto.Util.number import *

p = getPrime(64)
a = -1
b = 0

E = EllipticCurve(GF(p), [a, b])


G = E.gen(0)
print(G)