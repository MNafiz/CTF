from pwn import *

flag = b"redacted, t'as cru quoi??"
enc = open("output.bin", "rb").read()

key = xor(b"Securimag{", enc[:len(b"Securimag{")])

print(xor(enc,key).decode())