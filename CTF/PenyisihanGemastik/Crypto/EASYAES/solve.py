from pwn import *
from Crypto.Util.number import *


r = remote("ctf-gemastik.ub.ac.id", 10002 )

payload = b'a'*128
payload = bytes_to_long(payload)

r.sendlineafter(b"> ", b"1")

r.sendlineafter(b"= ", str(payload).encode())

r.recvuntil(b"= ")

ct = long_to_bytes(int(r.recvline(0)))

key = [xor(ct[i:i+16], b"a"*16) for i in range(0,128,16)]
key.append(xor(ct[128:144], b"\x10"*16))

r.sendlineafter(b"> ", b"2")

r.recvuntil(b"= ")

secret = long_to_bytes(int(r.recvline(0)))
secret = [secret[i:i+16] for i in range(0,144,16)]

secretplain = [xor(sec,keyy) for sec,keyy in zip(secret,key)]

guess = bytes_to_long(b"".join(secretplain)[:-16])


r.sendlineafter(b"> ", b"3")
r.sendline(str(guess).encode())

r.interactive()
