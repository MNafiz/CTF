#!/usr/bin/env python3
from Crypto.Util.number import *
from fastecdsa.curve import Curve
from fastecdsa.point import Point
from base64 import urlsafe_b64decode, urlsafe_b64encode
from time import time, sleep
from zlib import crc32


class BurveSigner:
    def __init__(self):
        self.C = Curve(
            "burvesigner",
            0xDB7C2ABF62E35E668076BEAD208B,
            0xDB7C2ABF62E35E668076BEAD2088,
            0x659EF8BA043916EEDE8911702B22,
            0xDB7C2ABF62E35E7628DFAC6561C5,
            0x0E27CD305696E88F38F7EB1FBECE,
            0xCAA9A6F90944FAD41FBE02B8FD77,
        )
        self.t = self.C.p.bit_length() // 8
        self.u = self.C.p.bit_length() - 64
        self.v = getRandomNBitInteger(self.u)

    def from_bytes(self, data):
        return int.from_bytes(data, "little")

    def to_bytes(self, num):
        return int.to_bytes(num, self.t, "little")

    def hash(self, msg):
        return crc32(msg)

    def set_keys(self):
        priv = open("./priv.data", "rb").read()[:self.t]
        self.x = self.from_bytes(priv)
        self.Y = self.x * self.C.G

    def get_params(self):
        self.set_keys()
        return {
            "p": self.C.p,
            "a": self.C.a,
            "b": self.C.b,
            "n": self.C.q,
            "G": (self.C.gx, self.C.gy),
            "Y": (self.Y.x, self.Y.y),
        }

    def sign(self, msg):
        self.set_keys()
        k = (int(time() * 1337) << self.u) + self.v
        R = k * self.C.G
        s = (self.hash(msg) - self.x * R.x) * pow(k, -1, self.C.q) % self.C.q
        sig = b"".join(map(self.to_bytes, [R.x, R.y, s]))
        return urlsafe_b64encode(sig)


    def verify(self, msg, sig):
        self.set_keys()
        try:
            assert len(sig) == 4 * self.t
            sig = urlsafe_b64decode(sig)
            arr = [sig[self.t * i : self.t * (i + 1)] for i in range(3)]
            Rx, Ry, s = map(self.from_bytes, arr)
            R = Point(Rx, Ry, self.C)
            return self.hash(msg) * self.C.G == s * R + self.Y * R.x
        except:
            return False


Signer = BurveSigner()
params = Signer.get_params()

p = params["p"]
a = params["a"]
b = params["b"]
n = params["n"]
Gx, Gy = params["G"]
Yx, Yy = params["Y"]
C = Curve("burvesigner", p=p, a=a, b=b, q=n, gx=Gx, gy=Gy)
Y = Point(Yx, Yy, C)
# print(C.G * 3)


t = C.p.bit_length() // 8
u = C.p.bit_length() - 64

def from_bytes(data):
    return int.from_bytes(data, "little")

def hash(data):
    return crc32(data)

payload1 = b"abcde"
payload2 = b"edcba"

sig1 = Signer.sign(payload1)
sig1 = urlsafe_b64decode(sig1)
Rx1, Ry1, s1 = map(from_bytes , [sig1[t * i : t * (i + 1)] for i in range(3)])
# print(s1)

sig2 = Signer.sign(payload2)
sig2 = urlsafe_b64decode(sig2)
Rx2, Ry2, s2 = map(from_bytes , [sig2[t * i : t * (i + 1)] for i in range(3)])
# print(s2)

R1 = Point(Rx1, Ry1 ,C)
R2 = Point(Rx2, Ry2 ,C)

for bf in range(1, 20000):
    diff = bf << u
    if R1 + diff * C.G == R2:
        print(diff, bf)
        break

# x = pow(Rx1 - Rx2, -1, C.q) * (s1 * diff - hash(payload2) + hash(payload1))
# x %= C.q

# k1 = (Rx1 * hash(payload2) - Rx1 * s2 * diff - Rx2 * hash(payload1)) * pow(Rx1 * s2 - s1 * Rx2, -1, C.q) % C.q
# x = (hash(payload1) - s1 * k1) * pow(Rx1 , -1 , C.q)
# x %= C.q

x = ((s1 * s2 * diff - s1 * hash(payload2) + s2 * hash(payload1)) * pow(Rx1 * s2 - Rx2 * s1, -1, C.q)) % C.q

def to_bytes(num):
    return int.to_bytes(num, t, "little")


# print(Y)
# print(x * C.G)

def fakeSign(msg):
    k = 4269
    R = k * C.G
    s = (hash(msg) - x * R.x) * pow(k, -1, C.q) % C.q
    sig = b"".join(map(to_bytes, [R.x, R.y, s]))
    return urlsafe_b64encode(sig)

msg = b"admin=True"
sig3 = fakeSign(msg)

print(Signer.verify(msg,sig3))