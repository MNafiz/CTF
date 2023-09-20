from Crypto.Util.number import *
from pwn import *
from pkcs1 import emsa_pkcs1_v15
import json

r = remote("socket.cryptohack.org", 13391)

msg = "I am Mallory. own CryptoHack.org"
msgint = bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), 256))
payload  = dict()
payload["option"] = "get_signature"

payload = json.dumps(payload).encode()

r.sendline(payload)
r.recvuntil(b"domain.\n")

result = json.loads(r.recvline(0).decode())

signature = int(result["signature"],16)

n = signature - msgint

print(signature % n == msgint)

payload = dict()
payload["option"] = "verify"
payload["msg"] = msg
payload["N"] = hex(n)
payload["e"] = hex(1)

payload = json.dumps(payload).encode()

r.sendline(payload)

r.interactive()