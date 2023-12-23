from pwn import *
from Crypto.Util.number import *

NC = "13.229.150.169:34054".split(":")

m = 0xb00ce3d162f598b408e9a0f64b815b2f
a = 0xaaa87c7c30adc1dcd06573702b126d0d
c = 0xcaacf9ebce1cdf5649126bc06e69a5bb

r = remote(NC[0], NC[1])

def goto(n):
    r.sendlineafter(b": ", str(n).encode())


nama = bytes_to_long(b"Santa Claus")

inv_amin1 = inverse(a-1, m)
y = inv_amin1 * c

for i in range(120, 1000, 8):
    kanan = nama << i
    hasil = (-(y + kanan)) % m
    name_payload =   long_to_bytes(kanan+hasil)
    if b"Santa Claus" in name_payload:
        break

goto(2)
r.sendlineafter(b"name: ", name_payload)
token = (-y) % m
r.sendlineafter(b"token: ", hex(token)[2:].encode())
goto(4)

r.interactive()
