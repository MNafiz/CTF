from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import *
import json


def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def hash(data):
    data = pad(data, 16)
    print(data)
    out = b"\x00" * 16
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
    return out


key = b'W<\xab\n\xe8+\xf1\x11\x94\x03\xaf&\r\x800\x84'
print(len(key))
r = remote("socket.cryptohack.org", 13388)

print(r.recvline())
send = {"option": "sign", "message": ""}
send = json.dumps(send).encode()
r.sendline(send)

data = bytes.fromhex(json.loads(r.recvline().decode())["signature"])
admin = b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10admin=True'.hex()
key = b'admin=True\x06\x06\x06\x06\x06\x06'
out = bxor(AES.new(key, AES.MODE_ECB).encrypt(data), data).hex()

send = {"option": "get_flag", "signature": out, "message": admin}
send = json.dumps(send).encode()
r.sendline(send)

print(r.recvline())