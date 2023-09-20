from pwn import *
from Crypto.Util.number import *
import random
# from sympy.ntheory import discrete_log
from sympy.ntheory.factor_ import smoothness
from libnum import xgcd
from Crypto.Util.number import *
from sympy import factorint
import math, libnum


def babyGiant(g, h, p, brute):
    N = int(math.sqrt(brute)) + 1
    tampung = {}

    for i in range(1,N):
        hasil = pow(g,i,p)
        tampung[hasil] = i

    x = []

    for i in range(N):
        hasil = (pow(g,-i*N,p)*h)%p
        if hasil in tampung:
            x.append(i*N + tampung[hasil])
    return min(x)

def PohligHellman(g, h, p, faktors):
    rem = []
    modulus = []
    # faktors = [i for i in factorint(p - 1)]
    phi = math.prod(faktors)
    for faktor in faktors:
        multiplier = phi // faktor
        _g = pow(g, multiplier, p)
        _h = pow(h, multiplier, p)
        modulus.append(faktor)
        rem.append(babyGiant(_g, _h, p, faktor))
    return libnum.solve_crt(rem, modulus)

NC = "nc 103.152.242.235 9784".split()

# r = remote(NC[1], NC[2])

context.log_level = "warning"
# r = process("./soal.py")

while 69:
    try:
        r = remote(NC[1], NC[2])
        # r = process("./soal.py")

        def goto(n):
            r.sendlineafter(b">> ", str(n).encode())

        
        goto(3)
        exec(r.recvline(0))

        goto(4)
        r.recvuntil(b"= ")
        next_state1 = int(r.recvline(0))

        goto(4)
        r.recvuntil(b"= ")
        next_state2 = int(r.recvline(0))

        goto(5)
        r.recvuntil(b"= ")
        enc_flag = int(r.recvline(0))

        goto(1)
        exec(r.recvline(0))
                
        r.close()

        # isSmooth = smoothness(m-1)
        # if (isSmooth[0] != isSmooth[1]) or (isSmooth[0] > 2**32) or (max(list(factorint(m-1).values())) > 1):
        #     continue

        faktor = factorint(m-1)
        if (max(list(faktor.values())) > 1) or (max(list(faktor.keys())) > 2**32):
            continue

        c = next_state2 - pow(a, next_state1, m) % m

        state_flag = PohligHellman(a, (next_state1 - c) % m, m, faktor)
        print(state_flag)
        random.seed(state_flag)

        flag = long_to_bytes(random.getrandbits(1024) ^ enc_flag)

        if b"IFEST" in flag:
            print(flag.decode())
            break

    except Exception as e:
        continue

# IFEST23{enkripsi_pakai_wrth_encryption:_sebaiknya_jangan_terlalu_gegabah_XD}