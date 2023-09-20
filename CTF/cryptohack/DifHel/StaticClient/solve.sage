from sage.all import *
from Crypto.Util.number import *
from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


NC = "nc socket.cryptohack.org 13373".split()

r = remote(NC[1],NC[2])

r.recvuntil(b"parameters: ")

payload = dict()
payload["g"] = hex(2)
payload["A"] = hex(1)
payload["p"] = hex(getPrime(64))

payload = json.dumps(payload).encode()

r.sendline(payload)

r.recvuntil(b"you: ")
r.recvuntil(b"you: ")

result = json.loads(r.recvline(0))

# print(decrypt_flag(1,result["iv"],result["encrypted"]))

share_secret = int("a98ae627c64b128d28f1669bf5f9465ca023b0ac55bff104f866696f290e6fdff193548e191bcf0e69b3c23bc5fe6d14f3253868d43dc274740b44e00c57d2467d646cfeeea840ba9c4d02ef87d0167eec02167a9a9dd2c2abfd54211ed898f79d8428911712dc16cf8b66dfa30de7fb235b176ae8935f4514f4b1abc5b23553798f1b0ea663c110579508f02da7b213dc9a7f1dc53a8616450d1e92fc277938c9822121cdffd5d7bbed51c4e2fc0e5a08f606f17a3b62c95ed3ee71159c3cfe", 16)
ct = {"iv": "242c03002b0ae3241878769c22ce9042", "encrypted": "e18383f7b73ce60503f4f7419198b214b72f4f107efb2afea24965e0b6999834"}
print(decrypt_flag(share_secret, ct["iv"], ct["encrypted"]))
#crypto{n07_3ph3m3r4l_3n0u6h}
r.interactive()
