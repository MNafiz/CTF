from pwn import *
from Crypto.Util.number import *

NC = "nc 178.128.102.145 50001".split()

r = remote(NC[1], NC[2])

r.recvuntil(b"Encrypted flag: ")

rr, s = eval(r.recvline(0))

r.recvuntil(b"Bob public key: ")

n2, e, beta = eval(r.recvline(0))

r.sendlineafter(b": ", str(n2).encode())
r.sendlineafter(b": ", str(e).encode())
r.sendlineafter(b": ", str(beta).encode())

payload = b'a'

r.sendlineafter(b": ", payload)

r.recvuntil(b"Your ciphertext: ")

rr, ss = eval(r.recvline(0))


flag = long_to_bytes(s * pow(ss, -1, n2) * bytes_to_long(payload) % n2)
print(flag.decode())

r.interactive()