from Crypto.Util.number import *
from sage.all import *
import random
def encrypt(p):
	p=bin(p)[2:]
	p='0'*(len(p)%64)+p
	p=[int(p[i:i+16],2) for i in range(0,len(p),16)]
	key=random.getrandbits(16)
	p=[i^key for i in p]
	return p

flag=b'REDACTED'
p=getPrime(1024)
q=getPrime(1024)
e=0x10001
n=p*q

temp=p&((1<<37)-1)
p>>=81
p<<=81
p+=temp
p=encrypt(p)

flag=bytes_to_long(flag)
enc=pow(flag,e,n)
print(f'enc : {enc}')
print(f'n : {n}')
print(f'e : {e}')
print(f'leaked_p :{p}')
