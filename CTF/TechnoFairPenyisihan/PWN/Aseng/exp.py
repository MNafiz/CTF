from pwn import *

elf = context.binary = ELF("./chall_patched_patched")

p = process("./chall_patched_patched")

print(hex(elf.got.puts))
# 0x404080 note list
p.interactive()