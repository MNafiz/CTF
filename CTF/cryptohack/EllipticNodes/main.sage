from collections import namedtuple
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from sage.all import *

qx=2582928974243465355371953056699793745022552378548418288211138499777818633265
qy=2421683573446497972507172385881793260176370025964652384676141384239699096612

p = 4368590184733545720227961182704359358435747188309319510520316493183539079703
gx = 8742397231329873984594235438374590234800923467289367269837473862487362482
gy = 225987949353410341392975247044711665782695329311463646299187580326445253608
a = (qy ** 2 - gy ** 2 - qx ** 3 + gx ** 3) * inverse((qx - gx) % p, p) % p
b = (gy ** 2 - gx ** 3 - a * gx) % p
F = GF(p)
A.<x,y> = F[]
print(F['x'](x^3+a*x+b).factor())
c1 = 3115846653938504361650386437377404449680779872497727646346367670719915515442
c2 = 2810666857764293539402767964015657133595357252060455687347132657823581321982
c = (c1 - c2) % p
print("c =", c)
# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'


def check_point(P):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p


def point_inverse(P):
    if P == O:
        return P
    return Point(P.x, -P.y % p)


def point_addition(P, Q):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R


def double_and_add(P, n):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n = n // 2
    assert check_point(R)
    return R


G = Point(gx, gy)
Q = Point(x=2582928974243465355371953056699793745022552378548418288211138499777818633265, y=2421683573446497972507172385881793260176370025964652384676141384239699096612)
# f = x^3 + a*x + b
# _f = f.sub(x=x + c2)
P.<x> = GF(p)[]
f = x^3 + a*x + b
f_ = f.subs(x=x - c2)
Q_ = (Q.x + c2, Q.y)
G_ = (G.x + c2, G.y)
print(f_.factor())
t = GF(p)(c).square_root()
v = (Q_[1] + t*Q_[0])/(Q_[1] - t*Q_[0]) % p
u = (G_[1] + t*G_[0])/(G_[1] - t*G_[0]) % p
d = discrete_log(v, u)
print(long_to_bytes(d))