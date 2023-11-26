from sage.all import *
from sympy import factorint
import libnum

def babyGiant(g, h, p, brute):
    x = []
    for i in range(1, brute+1):
        if g**i == h:
            x.append(i)
            print("ada")
    return min(x)

def PohligHellman(g, h, p):
    rem = []
    modulus = []
    faktors = [i for i in factorint(int(p - 1))]
    print(faktors)
    phi = math.prod(faktors)
    for faktor in [3]:
        multiplier = phi // faktor
        _g = g**multiplier #pow(g, multiplier, p)
        _h = h**multiplier #pow(h, multiplier, p)
        modulus.append(faktor)
        rem.append(babyGiant(_g, _h, p, faktor))
    return libnum.solve_crt(rem, modulus)

p = 1719620105458406433483340568317543019584575635895742560438771105058321655238562613083979651479555788009994557822024565226932906295208262756822275663694111
Fp = GF(p)
g = Fp(2)
x = Fp(4270)
h = g^x

print(PohligHellman(g, h, p))