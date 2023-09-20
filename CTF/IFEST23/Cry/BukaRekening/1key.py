from Crypto.Util.number import *
import random


flag = b'IFEST23{REDACTED}'

p = getPrime(2048)
q = getPrime(2048)
e = 65537
n = p*q

rand = getPrime(1024)
rand1 = random.randint(21, 300)

eksponen = (inverse(e, (p-1)*(q-1))-1)//(2**rand1)
ppow = pow(random.randint(1, rand)*p**rand1 + 1, eksponen, n)

enkripsi = pow(bytes_to_long(flag),e,n)
print(f'n = {n}')
print(f'e = {e}')
print(f'ppow = {ppow}')
print(f'enkripsi = {enkripsi}')