'''
s1 k1 = h + r1 d
s2 (2 k1 + 3) = h + r2 d

(s1 k1 - h) / r1 = d
(2 s2 k1 + 3 s2 - h) / r2 = d

(s1 k1 - h) / r1 = (2 s2 k1 + 3 s2 - h) / r2
(s1 k1 - h) r2 = (2 s2 k1 + 3 s2 - h) r1
s1 k1 r2 - h r2 = 2 s2 k1 r1 + 3 s2 r1 - h r1
s1 k1 r2 - 2 s2 k1 r1 = 3 s2 r1 - h r1 + h r2
k1 (s1 r2 - 2 s2 r1) = 3 s2 r1 - h r1 + h r2
k1 = (3 s2 r1 - h r1 + h r2) / (s1 r2 - 2 s2 r1)
'''

from pwn import *
from fastecdsa import curve
from tqdm import tqdm

io = process(["python3", "server.py"])
# io = remote('localhost', 33303)
# io = remote('103.167.133.102', 33303)

def sig2ticket(sig):
    return f"{sig[0]:x}z{sig[1]:x}"

def ticket2sig(ticket):
    try:
        x = ticket.split("z")
        return (int(x[0], 16), int(x[1], 16))
    except:
        print("Tiket kamu rusak")
        exit()

def find_k(r1, s1, r2, s2, r3, s3):
    h = int(hashlib.sha256(b'ubud').hexdigest(), 16)
    for a in tqdm(range(100, 1000)):
        for b in range(100, 1000):
            k1 = (b * s2 * r1 - h * r1 + h * r2) * pow(s1 * r2 - a * s2 * r1, -1, curve.P256.q) % curve.P256.q
            k2 = (b * s3 * r2 - h * r2 + h * r3) * pow(s2 * r3 - a * s3 * r2, -1, curve.P256.q) % curve.P256.q
            if (a * k1 + b) % curve.P256.q == k2:
                print(f'Found! a={a}, b={b}')
                return k1

def find_d(r1, s1, k1):
    h = int(hashlib.sha256(b'ubud').hexdigest(), 16)
    d = (s1 * k1 - h) * pow(r1, -1, curve.P256.q) % curve.P256.q
    return d

def buat_tiket(dest, d):
    h = int(hashlib.sha256(dest).hexdigest(), 16)
    k = 1337
    R = k * curve.P256.G
    r = R.x % curve.P256.q
    s = pow(k, -1, curve.P256.q) * (h + r * d) % curve.P256.q
    return sig2ticket((r, s))

def beli_tiket():
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Destinasi: ', b'ubud')
    io.recvuntil(b'Tiket: ')
    ticket = io.recvline(0).decode()
    return ticket2sig(ticket)

def berangkat(ticket):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Destinasi: ', b'citayam')
    io.sendlineafter(b'Tiket: ', ticket.encode())
    io.recvline(0)
    return io.recvline(0).decode()

r1, s1 = beli_tiket()
r2, s2 = beli_tiket()
r3, s3 = beli_tiket()

print(f'r1 = {r1}\ns1 = {s1}')
print(f'r2 = {r2}\ns2 = {s2}')
print(f'r3 = {r3}\ns3 = {s3}')

k = find_k(r1, s1, r2, s2, r3, s3)
d = find_d(r1, s1, k)
print(f'k = {k}')
print(f'd = {d}')

ticket = buat_tiket(b'citayam', d)
flag = berangkat(ticket)
print(flag)

io.close()
