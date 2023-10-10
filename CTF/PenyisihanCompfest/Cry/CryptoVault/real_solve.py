from pwn import *
import ecdsa
import ecdsa.ellipticcurve as EC
import binascii
import ecdsa.util
import json

context.log_level = "debug"

curve = ecdsa.SECP256k1
G = curve.generator
n = G.order()
x = int('ce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f42', 16)
y = int('6080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868', 16)
Q = EC.Point(curve.curve, x, y)
PUBKEY = ecdsa.VerifyingKey.from_public_point(Q, curve)
pubKey = 0xce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f426080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868

r = process("./server.py")


# can control the hash message and set it to 0
# set r = s so (hash + r * d) * sinv . G equals to (0 * rinv + r * d * rinv) . G
# finally equals to d G that equals to public key or point Q, hence set the r value to x coordinate of point Q

data = dict()
data["message_hash"] = hex(0)
data["signature"] = hex(Q.x())[2:].zfill(64)*2

r.sendlineafter(b"here: ", json.dumps(data).encode())
flag = r.recvline(0).decode()
r.close()

print(flag)