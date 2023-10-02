

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_16 = Integer(16); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
from pwn import *
from Crypto.Util.number import *
import json


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from sympy.ntheory.residue_ntheory import discrete_log


r = remote('socket.cryptohack.org', "13378")

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

# (mul + 1).bit_length() >= p.bit_length() and
def smooth_p():
    mul = _sage_const_1 
    i = _sage_const_1 
    while _sage_const_1 :
        mul *= i
        if  isPrime(mul + _sage_const_1 ):
            return mul + _sage_const_1 
        i += _sage_const_1 

r.recvuntil(b"Intercepted from Alice: ")
res = json_recv()
p = int(res["p"], _sage_const_16 )
g = int(res["g"], _sage_const_16 )
A = int(res["A"], _sage_const_16 )

r.recvuntil(b"Intercepted from Bob: ")
res = json_recv()
B = int(res["B"], _sage_const_16 )

r.recvuntil(b"Intercepted from Alice: ")
res = json_recv()
iv = res["iv"]
ciphertext = res["encrypted"]

s_p = smooth_p()
# print(s_p.bit_length())

r.recvuntil(b"send him some parameters: ")
json_send({
    "p": hex(s_p),
    "g": hex(_sage_const_2 ),
    "A": hex(A)
    })


r.recvuntil(b"Bob says to you: ")
res = json_recv()
print(res)
F = GF(s_p)
B = F(int(res["B"], _sage_const_16 ))
b = B.log(g)
print(b,"dapet")

shared_secret = pow(A, b, p)


def is_pkcs7_padded(message):
    padding = message[-message[-_sage_const_1 ]:]
    return all(padding[i] == len(padding) for i in range(_sage_const_0 , len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:_sage_const_16 ]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, _sage_const_16 ).decode('ascii')
    else:
        return plaintext.decode('ascii')


print(decrypt_flag(shared_secret, iv, ciphertext))
