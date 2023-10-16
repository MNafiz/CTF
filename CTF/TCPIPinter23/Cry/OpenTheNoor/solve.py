from pwn import *
from Crypto.Util.Padding import pad, unpad

NC = "nc ctf.tcp1p.com 2223".split() 

# r = remote(NC[1], NC[2])

r = process("./chall.py")

def goto(n):
    r.sendlineafter(b"> ", str(n).encode())

def login(password):
    goto(1)
    r.sendlineafter(b"[?] ", password.hex().encode())

def ask_oracle(password):
    login(password)
    result = r.recvline(0)
    return result == b"[!] INTRUDER ALERT"

def retrieve():
    goto(3)
    r.recvuntil(b"[+] ")
    return r.recvline(0)

target = pad(b"nottheflagbutstillcrucialvalidation", 16)

for i in range(4):
    r.recvline()

passadmin = bytes.fromhex(r.recvline(0).decode())

enc_pass = retrieve()

print(len(enc_pass))

enc_pass_bytes = bytes.fromhex(enc_pass.decode())

blocks = [enc_pass_bytes[i:i+16] for i in range(0, len(enc_pass_bytes), 16)]

fullpass = b""

for i in range(1, len(blocks)):
    block_kiri = blocks[i-1]
    block_kanan = blocks[i]
    plain = b""
    block_akhir = b""
    for i in range(16):
        print(i)
        for j in range(256):
            iv_baru = b"\x00"*(15-i) + bytes([j]) + block_akhir
            if ask_oracle(iv_baru + block_kanan):
                plain = xor(bytes([j]), i+1, block_kiri[-(i+1)]) + plain
                block_akhir = xor(block_kiri[-(i+1):], plain, i+2)
                break

    print(plain, passadmin)
    fullpass += plain

print(fullpass, passadmin, fullpass == passadmin)
print(len(fullpass))

fullpass_blocks = [fullpass[i:i+16] for i in range(0, len(fullpass), 16)]
target_blocks = [target[i:i+16] for i in range(0, len(target), 16)]
print(target_blocks)
print(fullpass_blocks)

blocks[-2] = xor(blocks[-2], fullpass_blocks[-1], target_blocks[-1])

login(b"".join(blocks))

fullpass = b""

for i in range(1, len(blocks)):
    block_kiri = blocks[i-1]
    block_kanan = blocks[i]
    plain = b""
    block_akhir = b""
    for i in range(16):
        print(i)
        for j in range(256):
            iv_baru = b"\x00"*(15-i) + bytes([j]) + block_akhir
            if ask_oracle(iv_baru + block_kanan):
                plain = xor(bytes([j]), i+1, block_kiri[-(i+1)]) + plain
                block_akhir = xor(block_kiri[-(i+1):], plain, i+2)
                break

    print(plain, passadmin)
    fullpass += plain

print(fullpass, passadmin, fullpass == passadmin)

fullpass_blocks = [fullpass[i:i+16] for i in range(0, len(fullpass), 16)]

blocks[-3] = xor(blocks[-3], fullpass_blocks[-2], target_blocks[-2])

login(b"".join(blocks))

fullpass = b""

for i in range(1, len(blocks)):
    block_kiri = blocks[i-1]
    block_kanan = blocks[i]
    plain = b""
    block_akhir = b""
    for i in range(16):
        print(i)
        for j in range(256):
            iv_baru = b"\x00"*(15-i) + bytes([j]) + block_akhir
            if ask_oracle(iv_baru + block_kanan):
                plain = xor(bytes([j]), i+1, block_kiri[-(i+1)]) + plain
                block_akhir = xor(block_kiri[-(i+1):], plain, i+2)
                break

    print(plain, passadmin)
    fullpass += plain

print(fullpass, passadmin, fullpass == passadmin)

fullpass_blocks = [fullpass[i:i+16] for i in range(0, len(fullpass), 16)]

blocks[-4] = xor(blocks[-4], fullpass_blocks[-3], target_blocks[-3])

login(b"".join(blocks))

fullpass = b""

for i in range(1, len(blocks)):
    block_kiri = blocks[i-1]
    block_kanan = blocks[i]
    plain = b""
    block_akhir = b""
    for i in range(16):
        print(i)
        for j in range(256):
            iv_baru = b"\x00"*(15-i) + bytes([j]) + block_akhir
            if ask_oracle(iv_baru + block_kanan):
                plain = xor(bytes([j]), i+1, block_kiri[-(i+1)]) + plain
                block_akhir = xor(block_kiri[-(i+1):], plain, i+2)
                break

    print(plain, passadmin)
    fullpass += plain

print(fullpass, passadmin, fullpass == passadmin)

r.interactive()