import string
from hashlib import sha256
from pwn import *
import json


def _xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])


def _and(a, b):
    return bytes([_a & _b for _a, _b in zip(a, b)])


def shuffle(mixed_and, mixed_xor):
    return bytes([mixed_xor[i%len(mixed_xor)] for i in mixed_and])


alphabet = string.ascii_letters + string.digits + "{}_!@$^&"
FLAG = b"crypto{???????????????????????????????}"
size = len(FLAG)
for c in alphabet:
    print(c, ord(c) % size, end=", ")
print("")
r = remote("socket.cryptohack.org", 13402)

print(r.recvline())
li = {}
for c in alphabet:
    arr = []
    for i in range(1, 256):
        if ord(c) & i == 0:
            arr.append(i)
    li[c] = arr
flag = []
for i in range(size):
    flag.append([])
index = 0
flag = []
while True:
    arr = []
    for i in range(1, 256):
        data = b"\x00" * index + bytes([i]) + b"\x00" * (size - index - 1)
        send = {"option": "mix", "data": data.hex()}
        send = json.dumps(send).encode()
        r.sendline(send)
        rec = json.loads(r.recvline().decode())["mixed"]
        for j in range(256):
            very_mixed = bytes([j]) * size
            super_mixed = sha256(very_mixed).hexdigest()
            if rec == super_mixed:
                arr.append(i)
                break
    print(arr)
    c_arr = []
    for c in alphabet:
        check = True
        for i in range(len(li[c])):
            if not li[c][i] in arr:
                check = False
                break
        if check == True:
            c_arr.append(c)
    print(c_arr)
    if index == size - 1:
        break
    else:
        index += 1