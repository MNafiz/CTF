from sage.all import *
from Crypto.Util.number import *
from pwn import *
import json

NC = "nc socket.cryptohack.org 13386".split()
HOST = NC[1]
PORT = NC[2]

def gcd(a, b): 
    while b:
        a, b = b, a % b
    return a.monic()

def franklinreiter(C1, C2, e, N, a1, b1,a2,b2):
    P.<X> = PolynomialRing(Zmod(N))
    g1 = (a1*X + b1)^e - C1
    g2 = (a2*X + b2)^e - C2
    result = -gcd(g1, g2).coefficients()[0]
    return result

r = remote(HOST,PORT)

payload = dict()
payload["option"] = "get_flag"
payload = json.dumps(payload).encode()

r.sendline(payload)

r.recvuntil(b"flag.\n")

result = json.loads(r.recvline(0).decode())

n = result["modulus"]

a1, b1 = result["padding"][0],result["padding"][1]

c1 = result["encrypted_flag"]

payload = dict()
payload["option"] = "get_flag"
payload = json.dumps(payload).encode()

r.sendline(payload)


result = json.loads(r.recvline(0).decode())

print("selesai")

a2, b2 = result["padding"][0],result["padding"][1]
c2 = result["encrypted_flag"]

m = franklinreiter(c2,c1,11,n,a2,b2,a1,b1)

print(bytes.fromhex(hex(m)[2:]))

r.interactive()