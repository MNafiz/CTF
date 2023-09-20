from sage.all import *

R = GF(991)
g = R(209)

ans = g^(-1)

assert ans*g == 1

print(ans)
