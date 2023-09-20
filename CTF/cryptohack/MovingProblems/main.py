from ecdsa import ellipticcurve
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

p = 1331169830894825846283645180581
a = -35
b = 98
n = 103686954799254136375814
curve = ellipticcurve.CurveFp(p, a, b, 1)

A = ellipticcurve.PointJacobi(curve, 1110072782478160369250829345256, 800079550745409318906383650948, 1, n, generator=True)
G = ellipticcurve.PointJacobi(curve, 479691812266187139164535778017, 568535594075310466177352868412, 1, n, generator=True)
B = ellipticcurve.PointJacobi(curve, 1290982289093010194550717223760, 762857612860564354370535420319, 1, n // 2, generator=True)
print(G.x() % n, G.y() % n)
print(A.x() % n, A.y() % n)
print(B.x() % n, B.y() % n)
m = 29618469991922269
shared_secret = (m * B).x()
sha1 = hashlib.sha1()
sha1.update(str(shared_secret).encode('ascii'))
key = sha1.digest()[:16]
iv = bytes.fromhex('eac58c26203c04f68d63dc2c58d79aca')
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(bytes.fromhex('bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d')))