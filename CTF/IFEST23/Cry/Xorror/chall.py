import random
from Crypto.Util.number import *

def roror(m):
    for i in range(m, 1234567891011121314151617):
        m^=i
    return m

msg = open('message.txt','rb').read()

f = open('output.txt','w')
x = [random.randint(1,9) for i in range(len(msg))]
n = getPrime(64)
enc = [n]
for i in range(len(msg)):
    enc.append(msg[i]^((x[i]*roror(x[i]))%n))
f.write(str(enc))
f.write('\n')
f.close()