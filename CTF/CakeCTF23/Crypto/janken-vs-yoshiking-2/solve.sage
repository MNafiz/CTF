from sage.all import *
from pwn import *
from Crypto.Util.number import *
from sympy import factorint
import math, libnum

#CakeCTF{though_yoshiking_may_die_janken_will_never_perish}
def babyGiant(g, h, p, brute):
    x = []
    for i in range(1,brute+1):
        if g^i == h:
            x.append(i)
            print("ada")
            break
    return min(x)

def PohligHellman(g, h, p):
    rem = []
    modulus = []
    faktors = [i for i in factorint(int(p - 1))]
    print(faktors)
    phi = math.prod(faktors)
    for faktor in [3]:
        multiplier = phi // faktor
        _g = g^multiplier 
        _h = h^multiplier
        modulus.append(faktor)
        rem.append(babyGiant(_g, _h, p, faktor))
    return libnum.solve_crt(rem, modulus)



NC = "nc crypto.2023.cakectf.com 10555".split()

context.log_level = "warning"

for i in range(10):
    try:
        print(i+1)
        #r = remote(NC[1], NC[2])
        r = process("./server.sage")
        r.recvuntil(b"Here is p: ")
        p = int(r.recvuntil(b",", drop=True))
        r.recvuntil(b"M: ")
        M = eval(r.recvline(0))
        M = [M[i:i+5] for i in range(0, len(M), 5)]
        M = Matrix(GF(p), M)
        if M.is_diagonalizable():
            print("Dapet")
            break
    except Exception as e:
        print(e)
        r.close()
        continue

for i in range(100):
    try:
        print(i+1)
        r.recvuntil(b"my commitment is=")
        Mr = eval(r.recvline(0))
        Mr = [Mr[i:i+5] for i in range(0, len(Mr), 5)]
        Mr = Matrix(GF(p), Mr)
        ans = PohligHellman(M, Mr, p)
        r.sendlineafter(b": ", str(ans).encode())
    except:
        print("Gagal")
        exit()

r.interactive()
