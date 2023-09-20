from pwn import *

context.arch = "amd64"
elf = context.binary = ELF("./chall_patched")
r = process("./chall_patched")



sc = """mov rdx, 0x100
"""
sc = asm(sc)
print(len(sc))

gdb.attach(r)
pause()

r.sendline(sc*4)

r.interactive()