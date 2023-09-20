from sage.all import *
from Crypto.Util.number import *
from pwn import *


NC = "nc 103.152.242.235 9784".split()
r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b">> ", str(n).encode())

list_state = []
for i in range(5):
    goto(4)
    r.recvuntil(b"= ")
    list_state.append(int(r.recvline(0)))
print(list_state)


list_state_selisih_berdekatan  = [list_state[i] - list_state[i-1] for i in range(1, len(list_state))]
print(list_state_selisih_berdekatan)

print(list_state_selisih_berdekatan[0] + list_state_selisih_berdekatan[1])
print(list_state[2] - list_state[0])

r.interactive()