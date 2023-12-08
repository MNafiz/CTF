from sage.all import *
from pwn import *
from hashlib import sha256
from secrets import randbelow
from Crypto.Util.number import *

context.log_level = "warning"

class SHA256chnorr:

    def __init__(self, private_key):
        self.p = 0x184e26a581fca2893b2096528eb6103ac03f60b023e1284ebda3ab24ad9a9fe0e37b33eeecc4b3c3b9e50832fd856e9889f6c9a10cde54ee798a7c383d0d8d2c3  
        self.q = (self.p - 1) // 2
        self.g = 3
        self.x = private_key
        self.y = pow(self.g, self.x, self.p)

    def H(self, msg):
        return bytes_to_long(2 * sha256(msg).digest()) % self.q

    def sign(self, msg):
        k = self.H(msg + long_to_bytes(self.x))
        r = pow(self.g, k, self.p) % self.q
        e = self.H(long_to_bytes(r) + msg)
        s = (k - self.x * e) % self.q
        return (s, e)

    def verify(self, msg, sig):
        s, e = sig
        if not (0 < s < self.q):
            return False
        if not (0 < e < self.q):
            return False
        rv = pow(self.g, s, self.p) * pow(self.y, e, self.p) % self.p % self.q
        ev = self.H(long_to_bytes(rv) + msg)
        return ev == e

def sign(msg):
    r.sendlineafter(b"> ", b"S")
    r.sendlineafter(b"> ", msg.hex().encode())
    r.recvuntil(b"Signature: ")
    s, e = eval(r.recvline(0))
    return s, e

def verify(msg, s, e):
    r.sendlineafter(b"> ", b"V")
    r.sendlineafter(b"> ", msg.hex().encode())
    r.sendlineafter(b"> ", str(s).encode())
    r.sendlineafter(b"> ", str(e).encode())
    
def H(msg):
    return bytes_to_long(2 * sha256(msg).digest()) % q

for loop in range(1000):
    r = process(["python3", "server.py"])

    r.recvuntil(b"g: ")
    g = int(r.recvline(0))
    r.recvuntil(b"y: ")
    y = int(r.recvline(0))
    r.recvuntil(b"p: ")
    p = int(r.recvline(0))
    q = (p - 1) // 2

    Ss = []
    Es = []
    Ms = []

    for i in range(2):
        msg = bytes([97 + i])
        s, e = sign(msg)
        Ms.append(msg)
        Ss.append(s)
        Es.append(e)


    B = 2**256
    B_1_inv = inverse_mod(B+1, q)

    # Es = [i * inverse_mod(B+1, q) % q for i in Es]
    # Ss = [i * inverse_mod(B+1, q) % q for i in Ss]

    length = len(Es) + 2
    matrix = []
    for i in range(length - 2):
        matrix.append([0]*i + [q] + [0]*(length - i - 1))

    for i in range(2):
        matrix.append([0]*length)

    i = 0
    for s, e in zip(Ss, Es):
        matrix[length - 2][i] = e * B_1_inv 
        matrix[length - 1][i] = s * B_1_inv 
        i = i + 1

    matrix[length - 2][length - 2] = B / q
    matrix[length - 1][length - 1] = B 

    result = Matrix(QQ, matrix).LLL()

    for row in result:
        if row[-1] == B:
            # print("Dapet Private Key ???")
            k0 = row[0]
            k1 = row[1]
            d_1 = ( (B+1) * k0 - Ss[0]) * inverse_mod(Es[0], q) % q
            d_2 = ( (B+1) * k1 - Ss[1]) * inverse_mod(Es[1], q) % q
            if d_1 == d_2:
                # print("Inikah?")
                fakeSigner = SHA256chnorr(d_1)
                msg = b"right hand"
                s, e = fakeSigner.sign(msg)
                verify(msg, s, e)
                break

    res = r.recvline(0).decode()
    r.close()
    print(res, loop+1)
    if "Invalid" not in res:
        break

