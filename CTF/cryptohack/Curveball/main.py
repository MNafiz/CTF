# from my_library import compute_2p, compute_kp
from Crypto.Util.number import long_to_bytes
from pwn import *
import json
p = int("ffffffff00000001000000000000000000000000ffffffffffffffffffffffff", 16)
a = int("0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc", 16)
b = int("0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
G = (int("0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16), int("0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16))
n = int("0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551", 16)
print("a =", a)
print("b =", b)
print("p =", p)
print("n =", n)
E = (int("0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531", 16), int("0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A", 16))
print(E)

r = remote("socket.cryptohack.org", 13382)
print(r.recvline())

send = {"private_key": n + 1, "host": 'www.bing.com', "curve": "secp256r1", "generator": [0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A]}
print(*send["generator"])
send = json.dumps(send).encode()
print(send)
r.sendline(send)
# {"private_key": 2, "host": "www.bing.com", "curve": "secp256r1", "generator": ["0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", "0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"]}
print(r.recvline())