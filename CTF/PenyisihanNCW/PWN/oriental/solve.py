#!/usr/bin/env python3

from pwn import *

exe = ELF("./oriental_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

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

    """
    0x00000000000012e3 : pop rdi ; ret
    0x00000000000012c8 : pop rdx ; ret
    0x00000000000012da : pop rsi ; ret
    """

    r.interactive()


if __name__ == "__main__":
    main()
