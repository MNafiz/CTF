from pwn import *
from hashlib import sha512
from Crypto.Util.number import inverse

def h(m):
    return int(sha512(m.encode()).hexdigest(), 16)

magic_word = "cake_does_not_eat_cat"
hash_magic_word = h(magic_word)

NC = "nc crypto.2023.cakectf.com 10444".split()

r = remote(NC[1], NC[2])

r.recvuntil(b"= ")
p = int(r.recvline(0))
r.recvuntil(b"= ")
g = int(r.recvline(0))
r.recvuntil(b"= ")
w, v = eval(r.recvline(0))
print(w,v)

"""
a*w - b * v = m mod (p - 1)
b*v = a*w - m mod (p - 1)
b = ((a*w) - m) vinv mod (p - 1) 
"""

a = 3
b = ((a * w) - hash_magic_word) * inverse(v, p - 1) % (p - 1)

s, t = pow(g, a, p), pow(g, b, p)

r.sendlineafter(b": ", b"V")
r.sendlineafter(b": ", magic_word.encode())
r.sendlineafter(b": ", str(s).encode())
r.sendlineafter(b": ", str(t).encode())

r.interactive()