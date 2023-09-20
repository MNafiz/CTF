from pwn import *
from Crypto.Util.number import isPrime
import json

r = remote("socket.cryptohack.org", 13392)

print(r.recvline())

p = 1042949915673747639548394979539773519387432406920217853474982925582324441002369106807062644005773384014539089496972340217284225886262811961269251256830829063
print(isPrime(p))
send = {"option": "sign", "prime": str(p)}
send = json.dumps(send).encode()
r.sendline(send)

data = json.loads(r.recvline().decode())["signature"]
p2 = 1042949915673747639548394979539773519387432406920217853474982925582324441002369106807076447498466965142113959008696894268189128104207757197289383619865780743
send = {"option": "check", "prime": str(p2), "signature": data, "a": "71"}
send = json.dumps(send).encode()
r.sendline(send)

print(r.recvline())