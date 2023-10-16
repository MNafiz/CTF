from pwn import *
from Crypto.Util.number import *


NC = "nc ctf.tcp1p.com 13339".split()

r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b"> ", str(n).encode())

goto(2)
goto("-")
r.recvuntil(b"= ")
hasil_1 = int(r.recvline(0))

goto(2)
goto("%")
r.recvuntil(b"= ")
hasil_2 = int(r.recvline(0))

result_1  =  hasil_2 - hasil_1

goto(1)
goto("p")

goto(2)
goto("-")
r.recvuntil(b"= ")
hasil_1 = int(r.recvline(0))

goto(2)
goto("%")
r.recvuntil(b"= ")
hasil_2 = int(r.recvline(0))

result_2  =  hasil_2 - hasil_1


q = GCD(result_1, result_2)

print(q, isPrime(q))

d = inverse(0x10001, q - 1)

goto(3)
exec(r.recvline(0))

print(long_to_bytes(pow(c,d,q)))

r.interactive()