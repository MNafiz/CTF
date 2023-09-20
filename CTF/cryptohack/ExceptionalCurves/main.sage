from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
import hashlib
from sage.all import *

p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

E = EllipticCurve(GF(p), [a, b])


def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()[0]


b_x = 0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38
b_y = 0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf
B = E(b_x, b_y)
nA = 2200911270816846838022388357422161552282496835763864725672800875786994850585872907705630132325051034876291845289429009837283760741160188885749171857285407
secret = shared_secret(B, nA)
sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
iv = bytes.fromhex('719700b2470525781cc844db1febd994')
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(bytes.fromhex('335470f413c225b705db2e930b9d460d3947b3836059fb890b044e46cbb343f0'))
print(decrypted)
