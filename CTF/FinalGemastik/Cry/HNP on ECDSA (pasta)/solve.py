#!/usr/bin/env python3
from sage.all import *
from Crypto.Util.number import *
from fastecdsa.curve import Curve
from fastecdsa.point import Point
from base64 import urlsafe_b64decode, urlsafe_b64encode
from time import time, sleep
from zlib import crc32
from random import getrandbits, randint


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
        # priv = open("./priv.data", "rb").read()[:self.t]
        # self.x = self.from_bytes(priv)
        self.d = getrandbits(64)
        self.Y = self.d * self.C.G

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
        # self.set_keys()
        k = getrandbits(100)
        R = k * self.C.G
        s = (self.hash(msg) + self.d * R.x) * pow(k, -1, self.C.q) % self.C.q
        sig = b"".join(map(self.to_bytes, [R.x, R.y, s]))
        return urlsafe_b64encode(sig)


    def verify(self, msg, sig):
        # self.set_keys()
        try:
            assert len(sig) == 4 * self.t
            sig = urlsafe_b64decode(sig)
            arr = [sig[self.t * i : self.t * (i + 1)] for i in range(3)]
            Rx, Ry, s = map(self.from_bytes, arr)
            R = Point(Rx, Ry, self.C)
            return self.hash(msg) * self.C.G == s * R - self.Y * R.x
        except:
            return False

class FakeSigner:
    def __init__(self, d):
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
        self.d = d

    def from_bytes(self, data):
        return int.from_bytes(data, "little")

    def to_bytes(self, num):
        return int.to_bytes(num, self.t, "little")

    def hash(self, msg):
        return crc32(msg)

    def set_keys(self):
        # priv = open("./priv.data", "rb").read()[:self.t]
        # self.x = self.from_bytes(priv)
        self.Y = self.d * self.C.G

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
        # self.set_keys()
        k = getrandbits(64)
        R = k * self.C.G
        s = (self.hash(msg) + self.d * R.x) * pow(k, -1, self.C.q) % self.C.q
        sig = b"".join(map(self.to_bytes, [int(i) for i in [R.x, R.y, s]]))
        return urlsafe_b64encode(sig)


    def verify(self, msg, sig):
        # self.set_keys()
        try:
            assert len(sig) == 4 * self.t
            sig = urlsafe_b64decode(sig)
            arr = [sig[self.t * i : self.t * (i + 1)] for i in range(3)]
            Rx, Ry, s = map(self.from_bytes, arr)
            R = Point(Rx, Ry, self.C)
            return self.hash(msg) * self.C.G == s * R - self.Y * R.x
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

t = C.p.bit_length() // 8
u = C.p.bit_length() - 64

def from_bytes(data):
    return int.from_bytes(data, "little")

def hash(data):
    return crc32(data)

def get_public_sig(sig):
    sig = urlsafe_b64decode(sig)
    Rx2, Ry2, s2 = map(from_bytes , [sig[t * i : t * (i + 1)] for i in range(3)])
    return Rx2, Ry2, s2

# signature = Signer.sign(b"nafiz")
# print(signature)
# print(get_public_sig(signature), Signer.verify(b"nafiz", signature))

sigs = []
for i in range(100):
    signature = Signer.sign(b"nafiz")
    r, _, s = get_public_sig(signature)
    sigs.append((r, s))

h = hash(b"nafiz")

B = 2**100
length = len(sigs) + 2
matrix = []
for i in range(length - 2):
    matrix.append([0]*i + [n] + [0]*(length - i - 1))

for i in range(2):
    matrix.append([0]*length)

i = 0
for r, s in sigs:
    inv_s = inverse(s, n)
    matrix[length - 2][i] = r * inv_s
    matrix[length - 1][i] = h * inv_s
    i = i + 1

r0, s0 = sigs[0]

matrix[length - 2][length - 2] = B / n
matrix[length - 1][length - 1] = B 

result = Matrix(QQ, matrix).LLL()

for row in result:
    if row[-1] == B:
        print("Dapet Private Key ???")
        k0 = row[0]
        d = (k0 * s0 - h) * inverse(r0, n) % n
        fakeSigner = FakeSigner(d)
        msg = b"Transfer 1 juta bitcoin ke wallet saya dengan address : 0x4269"
        sigmsg = fakeSigner.sign(msg)
        if Signer.verify(msg, sigmsg):
            print("Siap akan ditransfer 1 juta bitcoin ke alamat 0x4269")
            break
        else:
            print("signaturenya gembel", d == Signer.d)

        # if d == Signer.d:
        #     print("Dapet private key")
        #     break

    # k0 = row[0]
    # d = (k0 * s0 - h) * inverse(r0, n) % n
    # if d == Signer.d:
    #     print("Dapet private key")


# print("\n".join([" ".join(str(i) for i in j) for j in matrix]))


