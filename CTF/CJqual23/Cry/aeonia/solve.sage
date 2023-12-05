from pwn import *
from sage.all import *
from Crypto.Util.number import *
from sympy import sqrt_mod, gcd

NC = "nc 178.128.102.145 50002".split()

r = remote(NC[1], NC[2])
r.recvuntil(b"Encrypted flag: ")
enc_flag = bytes.fromhex(r.recvline(0).decode())

p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
a = 0 
b = 7

def goto(n):
    r.sendlineafter(b"> ", str(n).encode())

def gen_key():
    goto(1)
    r.recvuntil(b"Private key: ")
    priv_key_user = r.recvline(0)
    r.recvuntil(b"Public key: ")
    pub_key_user = r.recvline(0)
    return priv_key_user, pub_key_user


priv_key_user, pub_key_user = gen_key()

def encrypt(pub):
    goto(2)
    r.sendlineafter(b"key: ", pub)
    r.sendlineafter(b": ", b"61")
    r.recvuntil(b"Shared ephemeral secret: ")
    return bytes.fromhex(r.recvline(0).decode())

def decompress(x, b):
    bit = int(x[0])
    x = bytes_to_long(x[1:])
    y = sqrt_mod(x**int(3) + int(b), int(p))
    if y == None:
        return None, None
    if Mod(y, 2) != Mod(bit, 2):
        y = p - y
    return x, y

def compress(x, y):
    bit = y % 2
    if bit == 1:
        result = "03" + hex(x)[2:].zfill(64)
    else:
        result = "02" + hex(x)[2:].zfill(64)
    return result.encode()

import math
bb = {
    10 : [10903, 5290657],
    14 : [109903,  383229727], #383229727 12977017
    16 : [3319, 22639],
    # 27 : [10833080827],
    32 : [199, 18979]
}


import math
perk = 1
for b in bb:
    perk *= math.prod(bb[b])

print(int(perk).bit_length())


Ebase = EllipticCurve(GF(p), [a, 7])
print(Ebase.order())

dlogs = []
faks = []

for b in bb:
    E = EllipticCurve(GF(p), [a, b])
    G = E.gen(0)
    order = E.order()
    for fak in bb[b]:
        point_small_order = G * (order // fak)
        x_mal, y_mal = list(point_small_order)[:-1]
        pub = "04" + hex(x_mal)[2:].zfill(64) + hex(y_mal)[2:].zfill(64)
        hasil = encrypt(pub.encode())
        x, y = decompress(hasil, b)
        scalar_mult_point_small_order = E(x, y)
        log = point_small_order.discrete_log(scalar_mult_point_small_order)
        dlogs.append(log)
        faks.append(fak)
        print(log)


d = CRT_list(dlogs, faks)
print(hex(d)[2:])
print(enc_flag.hex())
print(int(d).bit_length())

goto(3)
r.sendlineafter(b": ", hex(d)[2:].encode())
r.sendlineafter(b": ", enc_flag.hex().encode())
r.recvuntil(b"Decrypted message: ")

flag = bytes.fromhex(r.recvline(0).decode())

print(flag)

#CJ2023{real_world_crypto_3b8786f9}
r.interactive()