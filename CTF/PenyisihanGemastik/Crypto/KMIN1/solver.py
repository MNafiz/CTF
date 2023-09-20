from pwn import *
from sage.all import *


r = remote("ctf-gemastik.ub.ac.id", "10000")

r.recvuntil(b"k = ")

k = int(r.recvline(0))

shares = []

for i in range(k-1):
    x, y = r.recvline(0)[1:-1].split(b", ")
    x, y = int(x), int(y)
    shares.append((x,y))


x, y = shares[0]

guess = y % x


r.sendlineafter(b": ", str(guess).encode())

r.interactive()
