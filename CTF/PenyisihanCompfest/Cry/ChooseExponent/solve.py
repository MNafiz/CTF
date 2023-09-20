from pwn import *
from Crypto.Util.number import *
from libnum import xgcd

NC = "nc 34.101.122.7 10004".split()

while 69:
    try:
        r = remote(NC[1],NC[2])

        def getencflag(e):
            r.sendlineafter(b">> ", b"1")
            r.sendlineafter(b": ", str(e).encode())
            r.recvuntil(b"flag: ")
            c = int(r.recvline(0).decode())
            return c

        c3 = getencflag(3)
        c5 = getencflag(5)
        c7 = getencflag(7)

        r.close()

        n = GCD(GCD(c3*c7- c5**2, (c3*c5)**7 - c7**8), c5 * c7 - c3 ** 4)
        print(n.bit_length())
        if n.bit_length() <= 2050:
            flag = long_to_bytes((c3**2 * pow(c5, -1 , n))%n)
            if b"COMP" in flag:
                print(flag)
                break
        r.close()
    except:
        r.close()

