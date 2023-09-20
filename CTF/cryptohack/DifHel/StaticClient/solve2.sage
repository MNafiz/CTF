from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

context.log_level = "warning"

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

r.recvuntil(b"Alice: ")

result = json.loads(r.recvline(0))

r.recvuntil(b"Alice: ")

ct1 = json.loads(r.recvline(0))

payload = dict()
payload["g"] = result["A"]
payload["A"] = hex(1)
payload["p"] = result["p"]

payload = json.dumps(payload).encode()

r.sendline(payload)

# r.recvuntil(b"you: ")
# r.recvuntil(b"you: ")

r.recvuntil(b"you: ")

shared_secret = int(json.loads(r.recvline(0))["B"],16)

r.recvuntil(b"you: ")

ct2 = json.loads(r.recvline(0))

print(decrypt_flag(shared_secret,ct1["iv"],ct1["encrypted"]))
print(decrypt_flag(1,ct2["iv"],ct2["encrypted"]))
r.interactive()
