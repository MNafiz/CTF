from pwn import *
from Crypto.Util.number import *

NC = "nc 103.152.242.228 1021".split()


r = remote(NC[1], NC[2])

e = getPrime(16)
r.recvuntil(b"n : ")
n = int(r.recvline(0))
r.recvuntil(b"65537\n")

r.sendlineafter(b"e : ", str(e).encode())
d = int(r.recvline(0))
kphi = e*d - 1
d = inverse(65537, kphi)
print(d)

r.recvuntil(b"this")
r.recvline()
c = int(r.recvline(0))

m = pow(c, d, n)

# print(long_to_bytes(m))

r.sendline(str(m).encode())

r.interactive()