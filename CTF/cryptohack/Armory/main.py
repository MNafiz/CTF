import hashlib
from Crypto.Util.number import long_to_bytes, bytes_to_long


def _eval_at(poly, x, prime):
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


PRIME = 77793805322526801978326005188088213205424384389488111175220421173086192558047
point = (105622578433921694608307153620094961853014843078655463551374559727541051964080, 25953768581962402292961757951905849014581503184926092726593265745485300657424)
coefs = [long_to_bytes(point[0])]
for i in range(1):
    coef = hashlib.sha256(coefs[i - 1]).digest()
    coefs.append(coef)
coefs = [int.from_bytes(p, 'big') for p in coefs]
x = _eval_at(coefs, coefs[0], PRIME)
x = (point[1] - x * point[0]) % PRIME
coefs = [x] + coefs
print(long_to_bytes(x))