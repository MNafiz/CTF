from sage.all import *
from Crypto.Util.number import *
from gmpy2 import invert

teks = """
def add(G, P):
    return G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + P + P + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + \
        G + G + P + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + P + G + G + P + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + G + \
        G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + G + \
        G + G + G + G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + G + \
        G + G + G + G + G + P + G + G + G + G + G + G + G + G + G + G + P + G + G
"""

print(teks.count("P"))
print(teks.count("G"))

Q = (26326686390928441989926437302948364151298187886536227434090842323538336764500, 15057597490574272687879749163595226837809841897797118807290241444796596563842)

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
K = GF(p)
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(K, (a, b))

G = E.gens()[0]


n = E.order()
d = int(invert(21, n))
print(G)
print(n * G)
Q = E(Q)
P1 = Q - 288 * G
flag = bytes.fromhex(hex((d * P1).xy()[0])[2:])
print(flag)
