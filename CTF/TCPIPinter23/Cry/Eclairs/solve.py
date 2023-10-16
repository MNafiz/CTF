# from sage.all import *
from pwn import *
from random import getrandbits
from Crypto.Util.number import *

NC = "nc ctf.tcp1p.com 13341".split()

r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b">> ", str(n).encode())


def check(x):
    goto(1)
    r.sendlineafter(b"x: ", str(x).encode())
    return r.recvline(0)


goto(1)
r.recvuntil(b"parameter:\n")
ae = int(r.recvline(0))
be = int(r.recvline(0))
r.sendlineafter(b"x: ", b"0")


while 69:
    rand_1 = getrandbits(256)
    result = check(rand_1)
    if b"Not" not in result:
        xe_1, ye_1 = eval(result)
        break

while 69:
    rand_2 = getrandbits(256)
    result = check(rand_2)
    if b"Not" not in result:
        xe_2, ye_2 = eval(result)
        break


n = GCD(rand_1**3 - xe_1, rand_2**3 - xe_2)

for i in range(1, 100):
    if n % i == 0:
        n //= i

print(n.bit_length(), n)

# print(check(n+1))
# print(check(1))


print(check(ae))

r.interactive()