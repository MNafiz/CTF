from Crypto.Util.number import *
from libnum import xgcd
import random

p, q = getPrime(512), getPrime(512)
n = p*q
phi = (p - 1) * (q - 1)

d1 = getPrime(150)
e1 = random.randint(1,phi)
ed1 = e1 * d1 % phi

d2 = getPrime(150)
e2, k, _ = xgcd(d2,phi)
e2 = e2 * (phi + 1 - ed1) % phi
ed2