from Crypto.Util.number import *
from Crypto.PublicKey import RSA

message = b"_6009l3_4cc0un7}"
m = bytes_to_long(message)

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
d = getPrime(128)

while GCD(d, phi) != 1:
    d = getPrime(128)

e = inverse(d, phi)
c = pow(m, e, n)

key = RSA.construct((n, e))

print(key.export_key("PEM").decode())
for i in range(3): print()
print(f"{c = }")