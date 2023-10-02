from pwn import *
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from Crypto.Util.number import *
import json, hashlib

context.log_level = "warn"

g = generator_192
n = g.order()

def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return bytes_to_long(sha1_hash.digest())


NC = "nc socket.cryptohack.org 13381".split()

r = remote(NC[1], NC[2])

payload = dict()
payload["option"] = "sign_time"

r.sendlineafter(b"verify.\n", json.dumps(payload).encode())

sleep(0.04)

payload = json.loads(r.recvline(0))
brute = int(payload["msg"].split(":")[-1])
rr = int(payload["r"], 16)
s = int(payload["s"], 16)
hmsg = sha1(payload["msg"].encode())



for k in range(1, brute+1):
    secret = ((s * k  - hmsg) * pow(rr , -1, n)) % n
    pubkey = Public_key(g, g * secret)
    privkey = Private_key(pubkey, secret)
    sig = privkey.sign(hmsg, k)
    if sig.r == rr:
        print("Found !", secret)
        break

sig = privkey.sign(sha1(b"unlock"), 4269)
payload = dict()
payload["option"] = "verify"
payload["msg"] = "unlock"
payload["r"] = hex(sig.r)
payload["s"] = hex(sig.s)

r.sendline(json.dumps(payload).encode())
print(json.loads(r.recvline(0))["flag"])
r.close()