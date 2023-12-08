from pwn import *
from Crypto.Util.number import *

r = process(["python3", "server.py"])

def get_c_and_pubkey():
    r.sendlineafter(b"? ", b"y")
    r.recvuntil(b"key: ")
    n, e = eval(r.recvline(0))
    r.recvuntil(b"flag: ")
    ct = int(r.recvline(0))
    return n , e, ct

n1, e1, ct1 = get_c_and_pubkey()
n2, e2, ct2 = get_c_and_pubkey()

p = GCD(n1, n2)
q = n1 // p
d = pow(e1, -1, (p - 1) * (q - 1))
m = pow(ct1, d, n1)

flag = long_to_bytes(m).decode()

print(flag)

r.interactive()