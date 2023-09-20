import json
import requests
from pwn import*
import os
#!/usr/bin/env python3

HOST = "socket.cryptohack.org"
PORT = 13370

r = remote(HOST, PORT)
receive = r.recvline()
send = json.dumps({"msg": "request"}).encode()


def rc():
    r.sendline(send)
    first_rc = r.recvline().decode()
    if "error" in first_rc:
        return -1
    first_rc = json.loads(first_rc)["ciphertext"].encode()
    return base64.b64decode(first_rc)


arr = [[0 for i in range(256)] for j in range(20)]
for i in range(10000):
    xored = rc()
    if xored == -1:
        continue
    for j in range(20):
        arr[j][xored[j]] += 1

for i in range(20):
    for j in range(33, 127):
        if arr[i][j] == 0:
            print(chr(j), end='   ')
    print('\n')

# crypto{unr4nd0m_07p}