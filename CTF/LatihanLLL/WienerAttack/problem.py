from Crypto.Util.number import *

flag = b"Gemastik23{just_use_LLL_right?}"
m = bytes_to_long(flag)

p = getPrime(1024)
q = getPrime(1024)
n = p*q
phi = (p-1)*(q-1)
d = getPrime(32)
e = inverse(d,phi)

c = pow(m,e,n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")