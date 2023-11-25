from sage.all import *
from pwn import *
from randcrack import RandCrack
from Crypto.Util.number import *

def gcd(a, b): 
    while b:
        a, b = b, a % b
    return a.monic()

def franklinreiter(C1, C2, e, N, a, b):
    P.<X> = PolynomialRing(Zmod(N))
    g1 = (X + a)^e - C1
    g2 = (X + b)^e - C2
    result = -gcd(g1, g2).coefficients()[0]
    return result

rc = RandCrack()

NC = "nc 103.145.226.209 1928".split()

r = remote(NC[1], NC[2])

# r = process(["python3", "notsimple.py"])
e = 17

def goto(n):
    r.sendlineafter(b">> ", str(n).encode())

def wadidawe():
    goto(1)
    r.recvuntil(b"wadidaw = ")
    result = int(r.recvline(0), 16)
    # r.recvuntil(b"wadidaw_asli = ")
    # result_list = eval(r.recvline(0))
    return result

r.sendlineafter(b"e = ", str(e).encode())

# hasil = []
# res1, res2 = wadidaw()
# print(hex(res1))
# mask = 128
# for j in range(4):
#     res1_temp = res1 >> mask
#     hasil.append(res1_temp % (1 << 32))
#     mask *= 2

# print(hasil)
# print(res2)
# print(hex(res1))

for i in range(156):
    print(i+1)
    res1 = wadidawe()
    rc.submit((res1 >> 128) % (2**32))
    rc.submit((res1 >> 256) % (2**32))
    rc.submit((res1 >> 512) % (2**32))
    rc.submit((res1 >> 1024) % (2**32))


def wow(rc):
    wow = [rc.predict_getrandbits(32) << (128*pow(2,i)) for i in range(0, 4)]
    wadidaw = 0
    for i in wow:
        wadidaw |= i
    wiw = [wow[i] >> (128*pow(2,i)) for i in range(0, 4)]
    return wadidaw




print(wow(rc) == wadidawe())

goto(2)

r.recvuntil(b"c = ")
c1 = int(r.recvline(0))
r.recvuntil(b"n = ")
n = int(r.recvline(0))
a = wow(rc)

goto(2)
r.recvuntil(b"c = ")
c2 = int(r.recvline(0))
b = wow(rc)


res = franklinreiter(c1, c2, e, n, a, b)
m = long_to_bytes(int(res))
print(m)
print(e)
print(n)

opr1, opr2 = m.split(b"bebek")
opr1, opr2 = bytes_to_long(opr1), bytes_to_long(opr2)


goto(3)

r.sendlineafter(b"opr1 = ", str(opr1).encode())
r.sendlineafter(b"opr2 = ", str(opr2).encode())

r.recvline(0)

r.recvuntil(b"n = ")
n = int(r.recvline(0))

r.recvuntil(b"e = ")
e = int(r.recvline(0))

r.recvuntil(b"c = ")
c = int(r.recvline(0))

p = GCD((pow(opr1, 7, n) * opr2**5) - 1, n)
q = n//p
print(p*q == n)
print(p != n)



c = c * pow(opr1, 6, n) * pow(opr2, 9, n) % n
phi = (p - 1) * (q - 1)
assert phi % 3 != 0

d = inverse(e*3 , phi)

omo = pow(c, d, n)
m = omo * pow(opr1, -1, n) * pow(opr2, -1, n) % n

kode = long_to_bytes(int(m))

print(kode)

r.sendline(kode)

r.interactive()