from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# r = process("./chall.py")


NC = "nc ctf.tcp1p.com 35257".split()
r = remote(NC[1], NC[2])

r.recvuntil(b"My message ")
encFlag = bytes.fromhex(r.recvline(0).decode())
print(len(encFlag))

# patokan = encFlag[-16:]

# plain = b"\x10"*16
# for i in range(999999+1):
#     key = (str(i).zfill(6)*4)[:16].encode()
#     cipher = AES.new(key, mode=AES.MODE_ECB)
#     if cipher.encrypt(plain) == patokan:
#         print(i)
#     if i % 100000 == 0:
#         print(i)

plain = b"\x10"*16
r.sendlineafter(b">> ", plain)

r.recvuntil(b"Steve: ")
encPlain = bytes.fromhex(r.recvline(0).decode())[:16]
print(len(encPlain))

kamus_1 = dict()
for i in range(999999+1):
    key = (str(i).zfill(6)*4)[:16].encode()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    kamus_1[cipher.encrypt(plain)] = key
    if i % 100000 == 0:
        print(i)


kamus_2 = dict()


for i in range(999999+1):
    key = (str(i).zfill(6)*4)[:16].encode()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    kamus_2[key] = cipher.decrypt(encPlain)
    if kamus_2[key] in kamus_1:
        print("Dapet")
        break
    if i % 100000 == 0:
        print(i)

r.close()

key2 = key
key1 = kamus_1[kamus_2[key]]

cipher = AES.new(key2, mode=AES.MODE_ECB)
encFlag = cipher.decrypt(encFlag)
cipher = AES.new(key1, mode=AES.MODE_ECB)
Flag = unpad(cipher.decrypt(encFlag), 16)
print(Flag.decode())