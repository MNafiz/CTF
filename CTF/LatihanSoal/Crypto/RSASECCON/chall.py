from Crypto.Util.number import *

flag = b"flag{test}"
m = bytes_to_long(flag)
e = 0x10001
p, q = getPrime(1024), getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
kphi = e*d - 1
print(kphi.bit_length())