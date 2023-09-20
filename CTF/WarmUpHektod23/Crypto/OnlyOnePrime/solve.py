from Crypto.Util.number import *

with open("output.txt","r") as f:
    exec(f.read())
    f.close()

p = gift

d = inverse(e, p - 1)

m = pow(c,d,p)
null_inverse = pow(256, -1 , p)



for i in range(1,100000):
    plain = long_to_bytes(m)
    if b"hacktoday" in plain:
        print(plain)
        break
    m = (m * null_inverse) % p