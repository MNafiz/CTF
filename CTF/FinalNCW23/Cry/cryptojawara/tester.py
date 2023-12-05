from pwn import *
from aes import *
import os

key = b"1234567890123456"

c = AES(key)

CTR = 1
nonce = os.urandom(12)
print(nonce)
a = c.encrypt(nonce + int.to_bytes(CTR, 4, 'big'))
print(a)

print(xor(nonce, a))