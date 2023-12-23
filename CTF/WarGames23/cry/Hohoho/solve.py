from pwn import *
from Crypto.Util.number import *

NC = "13.229.150.169:34053".split(":")

m = 0xb00ce3d162f598b408e9a0f64b815b2f
a = 0xaaa87c7c30adc1dcd06573702b126d0d
c = 0xcaacf9ebce1cdf5649126bc06e69a5bb

r = remote(NC[0], NC[1])

def goto(n):
    r.sendlineafter(b": ", str(n).encode())

def register(name):
    goto(1)
    r.sendlineafter(b"name: ", name)
    r.recvuntil(b"login: ")
    return int(r.recvline(0).decode(), 16)

token_0 = register(b"\x00")
token_1 = register(b"\x01")

get_arbitrary_token = lambda x : (token_0 + (token_1 - token_0) * bytes_to_long(x)) % m

token = get_arbitrary_token(b"Santa Claus")

goto(2)
r.sendlineafter(b"name: ", b"Santa Claus")
r.sendlineafter(b"token: ", hex(token)[2:].encode())
goto(4)

r.interactive()