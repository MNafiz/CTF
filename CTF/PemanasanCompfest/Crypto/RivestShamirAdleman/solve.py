from pwn import *
from Crypto.Util.number import *
from gmpy2 import iroot, next_prime

NC = "nc 34.101.174.85 10004".split()

r = remote(NC[1],NC[2])



for i in range(100):
    r.recvline()
    r.recvline()
    print(i+1)
    for _ in range(3):
        exec(r.recvline(0))

    if e == 3:
        ans = int(iroot(c,3)[0])
    elif isPrime(n):
        d = pow(e,-1,n-1)
        ans = pow(c,d,n)
    else:
        p = int(iroot(n,2)[0])
        while n % p != 0:
            p = int(next_prime(p))
        q = n // p
        d = pow(e,-1,(p-1)*(q-1))
        ans = pow(c,d,n)
    r.sendlineafter(b"answer: ", str(ans).encode())


r.interactive()