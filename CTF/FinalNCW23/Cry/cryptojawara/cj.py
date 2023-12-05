from aes import AES
from Crypto.Util.Padding import pad
import os

# flag = open("flag.txt", "r").read()

flag = "NCW23{1234567890123456}"
flag = flag[len("NCW23{"):flag.index("}")].encode()
assert len(flag) % 16 == 0
key = os.urandom(16)
c = AES(key)

def encrypt(m):
    nonce = os.urandom(12)
    if type(m) == str:
        m = m.encode()
    CTR = 1
    ct = b""
    for i in range(0, len(m), 16):
        keystream = c.encrypt(nonce + int.to_bytes(CTR, 4, 'big'))
        ct += bytes([a ^ b for a, b in zip(m[i:i+16], keystream)])
        CTR += 1
    return nonce.hex(), ct.hex()


print(f"gift: {encrypt(flag)}")
while True:
    try:
        print(encrypt(bytes.fromhex(input("plaintext (hex): "))), flush=True)
    except:
        print("something went wrong")
        break