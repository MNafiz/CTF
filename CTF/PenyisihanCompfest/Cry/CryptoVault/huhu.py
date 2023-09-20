from Crypto.Util.number import *

def pt_add(p, q, E):
    zero = (0, 0)
    if p == zero:
        return q
    elif q == zero:
        return p
    else:
        x1, y1 = p
        x2, y2 = q
        if x1 == x2 and y1 == -y2:
            return zero

        Ea, Ep = E['a'], E['p']
        if p != q:
            lmd = (y2 - y1) * inverse(x2 - x1, Ep)
        else:
            lmd = (3 * (x1**2) + Ea) * inverse(2 * y1, Ep)
        x3 = ((lmd**2) - x1 - x2) % Ep
        y3 = (lmd * (x1 - x3) - y1) % Ep
        return x3, y3


def scalar_mult(n, p, E):
    q, r = p, (0, 0)
    while n > 0:
        if n % 2 == 1:
            r = pt_add(r, q, E)
        q = pt_add(q, q, E)
        n //= 2
    return r

import ecdsa, hashlib

message = hashlib.sha1(b"").digest()
print(message.hex())
message = bytes_to_long(message)
curve = ecdsa.SECP256k1
k = 11
G = curve.generator
n = G.order()
pubKey = 0xce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f426080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868
R = k * G
r = R.x()
s = (inverse(k, n)) % n

r = long_to_bytes(r)
s = long_to_bytes(s)
print((r + s).hex())