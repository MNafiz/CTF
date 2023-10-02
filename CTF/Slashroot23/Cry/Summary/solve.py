from pwn import *
from Crypto.Util.number import *
import hashlib, string

NC = " 103.152.242.228 1011".split()

from itertools import product

wl_cmd = b'echo lol'
wl_hash = hashlib.sha1(wl_cmd).digest()[:3]

i = 1
for word in product(string.ascii_lowercase, repeat=10):
    print(i)
    i += 1
    cmd = f"echo {''.join(word)} | cat flag?txt"
    if hashlib.sha1(cmd.encode()).digest()[:3] == wl_hash:
        print(cmd)
        break

# os.system(cmd)

r = remote(NC[0], NC[1])

r.sendline(cmd)
r.interactive()