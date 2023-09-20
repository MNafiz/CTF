from __future__ import division
from __future__ import print_function

import random
import functools

# 12th Mersenne Prime
_PRIME = 2 ** 521 - 1
# The 13th Mersenne Prime is 2**521 - 1

_RINT = functools.partial(random.SystemRandom().randint, 0)

def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum

def make_random_shares(secret, minimum, shares, prime=_PRIME):
    """
    Generates a random shamir pool for a given secret, returns share points.
    """
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")
    poly = [secret] + [_RINT(prime - 1) for i in range(minimum - 1)]
    points = [(i, _eval_at(poly, i, prime))
              for i in range(1, shares + 1)]
    return points

def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1). This can
    be computed via the extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain this, the result will be such that: 
    den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv

def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p

def recover_secret(shares, prime=_PRIME):
    """
    Recover the secret from share points
    (points (x,y) on the polynomial).
    """
    if len(shares) < 3:
        raise ValueError("need at least three shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)

def main():
    """Main function"""
    secret = int("8b09cfc4696b91a1cc43372ac66ca36556a41499b495f28cc7ab193e32eadd30", 16)
    shares = make_random_shares(secret, minimum=3, shares=6)

    print('Secret:                                                     ',
          secret)
    print('Shares:')
    if shares:
        for share in shares:
            print('  ', share)

    print('Secret recovered from minimum subset of shares:             ',
          recover_secret(shares[:3]))
    print('Secret recovered from a different minimum subset of shares: ',
          recover_secret(shares[-3:]))

if __name__ == '__main__':
    # main()
    b_0 = int("01f321441454c99f8831702500803472064a8506686505d411f36e7a0af70be7a81c7a121ef441553ce6fdfe4c78bde37a1f9dba564a19026316967df4febced5f8c", 16)
    f_6 = int("0xcf5fbf2f223e134b294ff8997ff582cb8ab231eb1efed5960283813101ca6b44c71fd381e08a60440b31374153146041a2da4305febe1055bcb95bbca03071314e", 16)
    arr = [(2, 0), (3, 0), (4, 0), (5, 0), (6, f_6)]
    x_s, y_s = zip(*arr)
    print(_lagrange_interpolate(0, x_s, y_s, _PRIME))
    key = (_lagrange_interpolate(0, x_s, y_s, _PRIME) + b_0) % _PRIME
    print(hex(key))
    print(int("0x0", 16))