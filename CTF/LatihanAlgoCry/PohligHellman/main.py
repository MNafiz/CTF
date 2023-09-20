from Crypto.Util.number import *
from sympy import factorint
import math, libnum


def babyGiant(g, h, p, brute):
    N = int(math.sqrt(brute)) + 1
    tampung = {}

    for i in range(1,N):
        hasil = pow(g,i,p)
        tampung[hasil] = i

    x = []

    for i in range(N):
        hasil = (pow(g,-i*N,p)*h)%p
        if hasil in tampung:
            x.append(i*N + tampung[hasil])
    return min(x)

def PohligHellman(g, h, p):
    rem = []
    modulus = []
    faktors = [i for i in factorint(p - 1)]
    phi = math.prod(faktors)
    for faktor in faktors:
        multiplier = phi // faktor
        _g = pow(g, multiplier, p)
        _h = pow(h, multiplier, p)
        modulus.append(faktor)
        rem.append(babyGiant(_g, _h, p, faktor))
    return libnum.solve_crt(rem, modulus)


p = getPrime(64)
e = getPrime(32)
g = 2
h = pow(g, e, p)

dlog = PohligHellman(g, h, p)

print(dlog, e)
print(pow(g,dlog,p), h)