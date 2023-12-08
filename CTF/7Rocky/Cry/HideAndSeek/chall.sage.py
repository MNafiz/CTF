

# This file was *autogenerated* from the file chall.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593 = Integer(1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593); _sage_const_62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998 = Integer(62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998); _sage_const_1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211 = Integer(1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211); _sage_const_42 = Integer(42)
from sage.all import *
from Crypto.Util.number import bytes_to_long

FLAG = bytes_to_long(b"ECSC{jaog}")
proof.arithmetic(False)
p = _sage_const_1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593   
a = _sage_const_62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998 
b = _sage_const_1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211 
F = GF(p)
E = EllipticCurve(F, [a, b], names=('G',)); (G,) = E._first_ngens(1)
assert FLAG < G.order()
k = randrange(G.order())
P = k * G
Q = FLAG * P

res = []
for _ in range(_sage_const_42 ):
    a = randrange(G.order())
    b = randrange(G.order())
    res.append((a, b, a * P + b * Q))
print(res)

