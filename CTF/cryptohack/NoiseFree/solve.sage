from pwn import *
import json
from sage.all import *

NC = "nc socket.cryptohack.org 13411".split()

q = 0x10001

list_AdotS = set()
r = remote(NC[1],NC[2])

r.recvuntil(b"flag?\n")
A = []
b = []


payload = dict()
payload["option"] = "encrypt"
payload["message"] = 0

for i in range(64):
    print(i+1)
    r.sendline(json.dumps(payload).encode())
    result = json.loads(r.recvline(0))
    A.append(eval(result["A"]))
    b.append(eval(result["b"]))

A = Matrix(GF(0x10001), A)
b = vector(GF(0x10001), b)

S = A.solve_right(b)


payload = dict()
payload["option"] = "get_flag"

flag = ""
for i in range(32):
    payload["index"] = i
    r.sendline(json.dumps(payload).encode())
    result = json.loads(r.recvline(0))
    A = vector(GF(0x10001), eval(result["A"]))
    b = int(result["b"])
    flag += chr(b - A * S)
    print(flag)

print(flag)

r.interactive()
