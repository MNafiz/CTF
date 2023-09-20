from pwn import *
import json
from os import urandom
from Crypto.Cipher import AES

HOST = "socket.cryptohack.org"
PORT = 13399


r = remote(HOST, PORT)

received = r.recvline()
send = {'option': 'reset_connection'}
r.sendline(json.dumps(send).encode())

received = r.recvline()
s = '00000000000000000000000000000000' + '000000000000000000000000'
print(bytes.fromhex(s)[16:])
send = {'option': 'reset_password', 'token': s}
r.sendline(json.dumps(send).encode())

received = r.recvline()
print(received)
send = {'option': 'authenticate', 'password': ''}
for i in range(256):
    if i == 0:
        continue
    size_byte = bytes([i]) * 8
    send['password'] = size_byte.decode()
    r.sendline(json.dumps(send).encode())

    received = r.recvline().decode()
    print(received, i)
