

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_100 = Integer(100); _sage_const_999 = Integer(999); _sage_const_0 = Integer(0); _sage_const_16 = Integer(16); _sage_const_1 = Integer(1); _sage_const_1000 = Integer(1000)
from sage.all import *
from pwn import *
from fastecdsa import curve
import hashlib
import random
import time

class Healing:
    def __init__(self, d):
        self.c = curve.P256
        self.d = d
        self.Q = self.c.G * self.d
        self.k = random.randint(_sage_const_2 , self.c.q - _sage_const_2 )
        self.a = random.randint(_sage_const_100 , _sage_const_999 )
        self.b = random.randint(_sage_const_100 , _sage_const_999 )

    @staticmethod
    def sig2ticket(sig):
        return f"{sig[0]:x}z{sig[1]:x}"

    @staticmethod
    def ticket2sig(ticket):
        try:
            x = ticket.split("z")
            return (int(x[_sage_const_0 ], _sage_const_16 ), int(x[_sage_const_1 ], _sage_const_16 ))
        except:
            print("Tiket kamu rusak")
            exit()

    def refresh(self):
        self.k = (self.a * self.k + self.b) % self.c.q

    def beli_tiket(self, dest: bytes):
        self.refresh()
        z = int(hashlib.sha256(dest).hexdigest(), _sage_const_16 )
        R = self.k * self.c.G
        r = R.x % self.c.q
        s = pow(self.k, -_sage_const_1 , self.c.q) * (z + r * self.d) % self.c.q
        return self.sig2ticket((r, s))

    def berangkat(self, dest: bytes, ticket: str):
        r, s = self.ticket2sig(ticket)
        z = int(hashlib.sha256(dest).hexdigest(), _sage_const_16 )
        u1 = z * pow(s, -_sage_const_1 , self.c.q) % self.c.q
        u2 = r * pow(s, -_sage_const_1 , self.c.q) % self.c.q
        R = u1 * self.c.G + u2 * self.Q
        return r == R.x

r = process(["python3", "server.py"])

q = int(curve.P256.q)
Fq = GF(q)

def goto(n):
    r.sendlineafter(b"> ", str(n).encode())

def beli(dest):
    goto(_sage_const_1 )
    r.sendlineafter(b": ", dest)
    r.recvuntil(b"Tiket: ")
    return Healing.ticket2sig(r.recvline(_sage_const_0 ).decode())

def berangkat(dest, tiket):
    goto(_sage_const_2 )
    r.sendlineafter(b": ", dest)
    r.sendlineafter(b"Tiket: ", tiket)


sigs_r = []
sigs_s = []
zs = []
for dest in ["ubud", "canggu", "canggu"]:
    sigs = beli(dest.encode())
    sigs_r.append(sigs[_sage_const_0 ] % q)
    sigs_s.append(sigs[_sage_const_1 ] % q)
    zs.append(int(hashlib.sha256(dest.encode()).hexdigest(), _sage_const_16 ) % q)


solved = False
count = _sage_const_0 
for a in range(_sage_const_100 , _sage_const_1000 ):
    print(a+_sage_const_1 )
    up = sigs_s[_sage_const_0 ] * zs[_sage_const_1 ] - a * sigs_s[_sage_const_1 ] * zs[_sage_const_0 ]
    down = (a * sigs_r[_sage_const_0 ] * sigs_s[_sage_const_1 ] - sigs_s[_sage_const_0 ] * sigs_r[_sage_const_1 ]) % q
    down = inverse_mod(down, q)
    ss = sigs_s[_sage_const_0 ] * sigs_s[_sage_const_1 ] % q
    for b in range(_sage_const_100 , _sage_const_1000 ):
        d = (up - ss * b) * down % q
        d = int(d)
        k2 = (zs[_sage_const_1 ] + sigs_r[_sage_const_1 ] * d) * inverse_mod(sigs_s[_sage_const_1 ], q) % q
        k2 = int(k2)
        k3 = (zs[_sage_const_2 ] + sigs_r[_sage_const_2 ] * d) * inverse_mod(sigs_s[_sage_const_2 ], q) % q
        k3 = int(k3)
        if (a * k2 + b) % q == k3:
            print("Dapet")
            count += _sage_const_1 
            solved = True
            break
    if solved:
        break

fakeHealing = Healing(d)

tiketCitayam = fakeHealing.beli_tiket(b"citayam").encode()

berangkat(b"citayam", tiketCitayam)

r.interactive()

