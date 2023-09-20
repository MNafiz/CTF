from pwn import *
from gmpy2 import iroot
from Crypto.Util.number import *
from functools import reduce
from scipy.stats import ortho_group
import time,re, numpy as np

seedAwal = int(time.time()) * 100

r = process("./server.py")

e = 0x10001

for i in range(100):


    exec(r.recvline(0))
    exec(r.recvline(0))
    exec(r.recvline(0))
    exec(r.recvline(0))

    start = time.time()
    prod = reduce(lambda a,b : a*b, coefs)
    diffSquare = leak**2 - 4*prod*n
    diff = int(iroot(diffSquare,2)[0])
    p = GCD(diff+leak,n)
    q = n//p
    d = pow(e,-1,(p-1)*(q-1))
    m = pow(c,d,n)
    guess = long_to_bytes(m)
    end = time.time()

    r.sendlineafter(b"? ", guess)
    print(i+1,end-start)


r.interactive()