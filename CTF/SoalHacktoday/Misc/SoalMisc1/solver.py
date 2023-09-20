from pwn import *
from gmpy2 import iroot
from Crypto.Util.number import *
from functools import reduce
from scipy.stats import ortho_group
import time,re, numpy as np

seedAwal = int(time.time()) * 100

r = process("./server.py")

e = 0x10001

for i in range(1):


    exec(r.recvline(0))
    exec(r.recvline(0))
    exec(r.recvline(0))
    exec(r.recvline(0))

    start = time.time()
    prod = reduce(lambda a,b : a*b, coefs)
    diffSquare = leak**2 - 4*prod*n
    diff = int(iroot(diffSquare,2)[0])
    p = GCD(diff+leak,n)
    q = n//p
    d = pow(e,-1,(p-1)*(q-1))
    m = pow(c,d,n)
    guess = long_to_bytes(m)
    end = time.time()

    r.sendlineafter(b"? ", guess)
    print(i+1,end-start)

result = r.recvuntil(b"])")
awal = result.find(b"[") 
akhir = result.find(b"]")
exec(b"vektor = " + result[awal:akhir+1])

start = time.time()
for i in range(200):
    random.seed(seedAwal+i)
    mat = ortho_group.rvs(dim=200,random_state=random.randint(0,1<<32))
    result = np.dot(np.linalg.inv(mat),vektor)
    plain = ""
    for hasil in result:
        j = round(float(hasil))
        if 0 <= j <= 255:
            plain += chr(j)
    if "answer" in plain:
        print("Dapet")
        break
end = time.time()

waktu_inv = end-start

start = time.time()
for i in range(200):
    random.seed(seedAwal+i)
    mat = ortho_group.rvs(dim=200,random_state=random.randint(0,1<<32))
    result = np.dot(np.transpose(mat),vektor)
    plain = ""
    for hasil in result:
        j = round(float(hasil))
        if 0 <= j <= 255:
            plain += chr(j)
    if "answer" in plain:
        print("Dapet")
        break
end = time.time()

waktu_transpose = end-start

teks = re.findall("answer\{.*\}",plain)[0]
teks = teks[teks.find("{") + 1 : teks.find("}")]

print(teks)
print(waktu_inv)
print(waktu_transpose)

r.sendlineafter(b"? ",teks.encode())

r.interactive()