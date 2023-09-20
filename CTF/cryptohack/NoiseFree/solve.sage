from pwn import *
import json
from sage.all import *

NC = "nc socket.cryptohack.org 13411".split()

q = 0x10001

list_AdotS = set()
r = remote(NC[1],NC[2])

r.recvuntil(b"flag?\n")

payload = dict()
payload["option"] = "encrypt"
payload["message"] = 0

r.send(json.dumps(payload).encode())

result = json.loads(r.recvline(0))
exec("A = " + result["A"])
b = int(result["b"])

# flag = ""
# for i in range(1):
#     payload = dict()
#     payload["option"] = "get_flag"
#     payload["index"] = i
#     r.send(json.dumps(payload).encode())
#     result = json.loads(r.recvline(0))
#     b = int(result["b"])
#     flag += chr(b - AdotS)
#     print(flag)

r.interactive()