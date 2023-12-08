from sage.all import *
from Crypto.Util.number import *

f = open("output.txt", "rb")
out = f.read().rstrip()
f.close()

out = out.replace(b":", b",")
out = eval(out)

a1, b1, P1 = out[0]
a2, b2, P2 = out[1]

p = 1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593  
a = 62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998
b = 1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211
F = GF(p)
E.<G> = EllipticCurve(F, [a, b])

G_order = G.order()
G_factors = factor(G_order)

P1 = E(P1[:-1])
P2 = E(P2[:-1])

P = (b2 * P1 - b1 * P2) * inverse_mod(a1*b2 - a2*b1, G_order)
Q = (P1 - a1 * P) * inverse_mod(b1, G_order)

print(a1 * P + b1 * Q == P1)
print(a2 * P + b2 * Q == P2)

def dlog(G, nG):
    dlogs, new_factors = [], []

    for p, e in G_factors:
        print(p, e)
        new_factors.append(p ** e)
        t = G_order // new_factors[-1]
        dlogs.append(discrete_log(t * nG, t * G, operation='+'))

    return CRT(dlogs, new_factors)


FLAG = int(dlog(P, Q))

# FLAG = int(P.discrete_log(Q))


print(long_to_bytes(FLAG))

