from pwn import *

r = process("./tes.py")

r.recvuntil(b">> ")
r.sendline(b"aa\x07\t")
print(r.recvline())

r.interactive()