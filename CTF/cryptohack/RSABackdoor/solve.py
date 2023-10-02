import logging
import os
import sys
from math import gcd

from sage.all import EllipticCurve
from sage.all import Zmod
from sage.all import hilbert_class_polynomial

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

import logging

from sage.all import ZZ
from sage.all import Zmod
from sage.all import factor

lcm = lambda a, b : (a * b) // gcd(a, b)


def fast_crt(X, M, segment_size=8):
    """
    Uses a divide-and-conquer algorithm to compute the CRT remainder and least common multiple.
    :param X: the remainders
    :param M: the moduli (not necessarily coprime)
    :param segment_size: the minimum size of the segments (default: 8)
    :return: a tuple containing the remainder and the least common multiple
    """
    assert len(X) == len(M)
    assert len(X) > 0
    while len(X) > 1:
        X_ = []
        M_ = []
        for i in range(0, len(X), segment_size):
            if i == len(X) - 1:
                X_.append(X[i])
                M_.append(M[i])
            else:
                X_.append(crt(X[i:i + segment_size], M[i:i + segment_size]))
                M_.append(lcm(*M[i:i + segment_size]))
        X = X_
        M = M_

    return X[0], M[0]


def _polynomial_hgcd(ring, a0, a1):
    assert a1.degree() < a0.degree()

    if a1.degree() <= a0.degree() / 2:
        return 1, 0, 0, 1

    m = a0.degree() // 2
    b0 = ring(a0.list()[m:])
    b1 = ring(a1.list()[m:])
    R00, R01, R10, R11 = _polynomial_hgcd(ring, b0, b1)
    d = R00 * a0 + R01 * a1
    e = R10 * a0 + R11 * a1
    if e.degree() < m:
        return R00, R01, R10, R11

    q, f = d.quo_rem(e)
    g0 = ring(e.list()[m // 2:])
    g1 = ring(f.list()[m // 2:])
    S00, S01, S10, S11 = _polynomial_hgcd(ring, g0, g1)
    return S01 * R00 + (S00 - q * S01) * R10, S01 * R01 + (S00 - q * S01) * R11, S11 * R00 + (S10 - q * S11) * R10, S11 * R01 + (S10 - q * S11) * R11


def fast_polynomial_gcd(a0, a1):
    """
    Uses a divide-and-conquer algorithm (HGCD) to compute the polynomial gcd.
    More information: Aho A. et al., "The Design and Analysis of Computer Algorithms" (Section 8.9)
    :param a0: the first polynomial
    :param a1: the second polynomial
    :return: the polynomial gcd
    """
    # TODO: implement extended variant of half GCD?
    assert a0.parent() == a1.parent()

    if a0.degree() == a1.degree():
        if a1 == 0:
            return a0
        a0, a1 = a1, a0 % a1
    elif a0.degree() < a1.degree():
        a0, a1 = a1, a0

    assert a0.degree() > a1.degree()
    ring = a0.parent()

    # Optimize recursive tail call.
    while True:
        logging.debug(f"deg(a0) = {a0.degree()}, deg(a1) = {a1.degree()}")
        _, r = a0.quo_rem(a1)
        if r == 0:
            return a1.monic()

        R00, R01, R10, R11 = _polynomial_hgcd(ring, a0, a1)
        b0 = R00 * a0 + R01 * a1
        b1 = R10 * a0 + R11 * a1
        if b1 == 0:
            return b0.monic()

        _, r = b0.quo_rem(b1)
        if r == 0:
            return b1.monic()

        a0 = b1
        a1 = r


def polynomial_gcd_crt(a, b, factors):
    """
    Uses the Chinese Remainder Theorem to compute the polynomial gcd modulo a composite number.
    :param a: the first polynomial
    :param b: the second polynomial
    :param factors: the factors of m (tuples of primes and exponents)
    :return: the polynomial gcd modulo m
    """
    assert a.base_ring() == b.base_ring() == ZZ

    gs = []
    ps = []
    for p, _ in factors:
        zmodp = Zmod(p)
        gs.append(fast_polynomial_gcd(a.change_ring(zmodp), b.change_ring(zmodp)).change_ring(ZZ))
        ps.append(p)

    g, _ = fast_crt(gs, ps)
    return g


def polynomial_xgcd(a, b):
    """
    Computes the extended GCD of two polynomials using Euclid's algorithm.
    :param a: the first polynomial
    :param b: the second polynomial
    :return: a tuple containing r, s, and t
    """
    assert a.base_ring() == b.base_ring()

    r_prev, r = a, b
    s_prev, s = 1, 0
    t_prev, t = 0, 1

    while r:
        try:
            q = r_prev // r
            r_prev, r = r, r_prev - q * r
            s_prev, s = s, s_prev - q * s
            t_prev, t = t, t_prev - q * t
        except RuntimeError:
            raise ArithmeticError("r is not invertible", r)

    return r_prev, s_prev, t_prev


def polynomial_inverse(p, m):
    """
    Computes the inverse of a polynomial modulo a polynomial using the extended GCD.
    :param p: the polynomial
    :param m: the polynomial modulus
    :return: the inverse of p modulo m
    """
    g, s, t = polynomial_xgcd(p, m)
    return s * g.lc() ** -1


def max_norm(p):
    """
    Computes the max norm (infinity norm) of a polynomial.
    :param p: the polynomial
    :return: a tuple containing the monomial degrees of the largest coefficient and the coefficient
    """
    max_degs = None
    max_coeff = 0
    for degs, coeff in p.dict().items():
        if abs(coeff) > max_coeff:
            max_degs = degs
            max_coeff = abs(coeff)

    return max_degs, max_coeff

def factorize(N, D):
    """
    Recovers the prime factors from a modulus using Cheng's elliptic curve complex multiplication method.
    More information: Sedlacek V. et al., "I want to break square-free: The 4p - 1 factorization method and its RSA backdoor viability"
    :param N: the modulus
    :param D: the discriminant to use to generate the Hilbert polynomial
    :return: a tuple containing the prime factors
    """
    assert D % 8 == 3, "D should be square-free"

    zmodn = Zmod(N)
    pr = zmodn["x"]

    H = pr(hilbert_class_polynomial(-D))
    Q = pr.quotient(H)
    j = Q.gen()

    try:
        k = j * polynomial_inverse((1728 - j).lift(), H)
    except ArithmeticError as err:
        # If some polynomial was not invertible during XGCD calculation, we can factor n.
        p = gcd(int(err.args[1].lc()), N)
        return int(p), int(N // p)

    E = EllipticCurve(Q, [3 * k, 2 * k])
    while True:
        x = zmodn.random_element()

        logging.debug(f"Calculating division polynomial of Q{x}...")
        z = E.division_polynomial(N, x=Q(x))

        try:
            d, _, _ = polynomial_xgcd(z.lift(), H)
        except ArithmeticError as err:
            # If some polynomial was not invertible during XGCD calculation, we can factor n.
            p = gcd(int(err.args[1].lc()), N)
            return int(p), int(N // p)

        p = gcd(int(d), N)
        if 1 < p < N:
            return int(p), int(N // p)
        
n = 709872443186761582125747585668724501268558458558798673014673483766300964836479167241315660053878650421761726639872089885502004902487471946410918420927682586362111137364814638033425428214041019139158018673749256694555341525164012369589067354955298579131735466795918522816127398340465761406719060284098094643289390016311668316687808837563589124091867773655044913003668590954899705366787080923717270827184222673706856184434629431186284270269532605221507485774898673802583974291853116198037970076073697225047098901414637433392658500670740996008799860530032515716031449787089371403485205810795880416920642186451022374989891611943906891139047764042051071647203057520104267427832746020858026150611650447823314079076243582616371718150121483335889885277291312834083234087660399534665835291621232056473843224515909023120834377664505788329527517932160909013410933312572810208043849529655209420055180680775718614088521014772491776654380478948591063486615023605584483338460667397264724871221133652955371027085804223956104532604113969119716485142424996255737376464834315527822566017923598626634438066724763559943441023574575168924010274261376863202598353430010875182947485101076308406061724505065886990350185188453776162319552566614214624361251463
e = 65537
c = 608484617316138126443275660524263025508135383745665175433229598517433030003704261658172582370543758277685547533834085899541036156595489206369279739210904154716464595657421948607569920498815631503197235702333017824993576326860166652845334617579798536442066184953550975487031721085105757667800838172225947001224495126390587950346822978519677673568121595427827980195332464747031577431925937314209391433407684845797171187006586455012364702160988147108989822392986966689057906884691499234298351003666019957528738094330389775054485731448274595330322976886875528525229337512909952391041280006426003300720547721072725168500104651961970292771382390647751450445892361311332074663895375544959193148114635476827855327421812307562742481487812965210406231507524830889375419045542057858679609265389869332331811218601440373121797461318931976890674336807528107115423915152709265237590358348348716543683900084640921475797266390455366908727400038393697480363793285799860812451995497444221674390372255599514578194487523882038234487872223540513004734039135243849551315065297737535112525440094171393039622992561519170849962891645196111307537341194621689797282496281302297026025131743423205544193536699103338587843100187637572006174858230467771942700918388

print(factorize(n, 427))