from pwn import *


NC = "nc 103.152.118.120 6868".split()

r = remote(NC[1], NC[2])

r.interactive()