from sage.all import *
from pwn import *
from Crypto.Util.number import *
from sympy import factorint
import math, libnum


NC = "nc crypto.2023.cakectf.com 10555".split()

context.log_level = "warning"

#r = remote(NC[1], NC[2])
r = process("./server.sage")
r.recvuntil(b"Here is p: ")
p = int(r.recvuntil(b",", drop=True))
Fp = GF(p)
r.recvuntil(b"M: ")
M = eval(r.recvline(0))
M = [M[i:i+5] for i in range(0, len(M), 5)]
M = Matrix(Fp, M)
k = M.charpoly().splitting_field('x')
J, P = M.jordan_form(k, transformation=True)
base = Mod(J[0][0], p)


for i in range(100):
        print(i+1)
        r.recvuntil(b"my commitment is=")
        Mr = eval(r.recvline(0))
        Mr = [Mr[i:i+5] for i in range(0, len(Mr), 5)]
        Mr = Matrix(GF(p), Mr)
        target = Mod((~P * Mr * P)[0][0], p)
        ans = discrete_log(target, base) % 3
        if ans == 0:
            ans = 3
        r.sendlineafter(b": ", str(ans).encode())

r.interactive()
