from pwn import *
from fastecdsa import curve
from Crypto.Util.number import *
from tqdm import tqdm
import hashlib
import random

class Healing:
    def __init__(self, d):
        self.c = curve.P256
        self.d = d
        self.Q = self.c.G * self.d
        self.k = random.randint(2, self.c.q - 2)
        self.a = random.randint(100, 999)
        self.b = random.randint(100, 999)

    @staticmethod
    def sig2ticket(sig):
        return f"{sig[0]:x}z{sig[1]:x}"

    @staticmethod
    def ticket2sig(ticket):
        try:
            x = ticket.split("z")
            return (int(x[0], 16), int(x[1], 16))
        except:
            print("Tiket kamu rusak")
            exit()

    def refresh(self):
        self.k = (self.a * self.k + self.b) % self.c.q

    def beli_tiket(self, dest: bytes):
        self.refresh()
        z = int(hashlib.sha256(dest).hexdigest(), 16)
        R = self.k * self.c.G
        r = R.x % self.c.q
        s = pow(self.k, -1, self.c.q) * (z + r * self.d) % self.c.q
        return self.sig2ticket((r, s))

    def berangkat(self, dest: bytes, ticket: str):
        r, s = self.ticket2sig(ticket)
        z = int(hashlib.sha256(dest).hexdigest(), 16)
        u1 = z * pow(s, -1, self.c.q) % self.c.q
        u2 = r * pow(s, -1, self.c.q) % self.c.q
        R = u1 * self.c.G + u2 * self.Q
        return r == R.x

r = process(["python3", "server.py"])

q = int(curve.P256.q)

def goto(n):
    r.sendlineafter(b"> ", str(n).encode())

def beli(dest):
    goto(1)
    r.sendlineafter(b": ", dest)
    r.recvuntil(b"Tiket: ")
    return Healing.ticket2sig(r.recvline(0).decode())

def berangkat(dest, tiket):
    goto(2)
    r.sendlineafter(b": ", dest)
    r.sendlineafter(b"Tiket: ", tiket)


sigs_r = []
sigs_s = []
zs = []
for dest in ["ubud", "canggu", "canggu"]:
    sigs = beli(dest.encode())
    sigs_r.append(sigs[0] % q)
    sigs_s.append(sigs[1] % q)
    zs.append(int(hashlib.sha256(dest.encode()).hexdigest(), 16) % q)


solved = False

inv_s1 = inverse(sigs_s[1], q)
inv_s2 = inverse(sigs_s[2], q)
for a in tqdm(range(100, 1000)):
    up = sigs_s[0] * zs[1] - a * sigs_s[1] * zs[0]
    down = (a * sigs_r[0] * sigs_s[1] - sigs_s[0] * sigs_r[1]) % q
    down = inverse(down, q)
    ss = sigs_s[0] * sigs_s[1] % q
    for b in range(100, 1000):
        d = (up - ss * b) * down % q
        d = int(d)
        k2 = (zs[1] + sigs_r[1] * d) * inv_s1 % q
        k2 = int(k2)
        k3 = (zs[2] + sigs_r[2] * d) * inv_s2 % q
        k3 = int(k3)
        if (a * k2 + b) % q == k3:
            solved = True
            break
    if solved:
        break

fakeHealing = Healing(d)

tiketCitayam = fakeHealing.beli_tiket(b"citayam").encode()

berangkat(b"citayam", tiketCitayam)

r.interactive()