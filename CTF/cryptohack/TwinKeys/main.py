from Crypto.Hash import MD5
from pwn import *
import json

file = open("collision1.bin", "rb")
a = file.read()

file = open("collision2.bin", "rb")
b = file.read()

r = remote("socket.cryptohack.org", 13397)

print(r.recvline())
send = {"option": "insert_key", "key": a.hex()}
send = json.dumps(send).encode()
r.sendline(send)

print(r.recvline())
send = {"option": "insert_key", "key": b.hex()}
send = json.dumps(send).encode()
r.sendline(send)

print(r.recvline())
send = {"option": "unlock"}
send = json.dumps(send).encode()
r.sendline(send)

print(r.recvline())
key = {"a": 0, "b": 1}
print(sum(key.values()))