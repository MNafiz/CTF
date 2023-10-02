from pwn import *

NC = "nc 103.152.242.228 2022".split()

r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b": ", str(n).encode())

for j in range(120):
    goto(2)
    for i in range(35):
        goto(3)

r.interactive()
#btn;szm~;~ziu~\x7f;os~;\x7fiz|tu;hwzb~i;zxsr~m~v~uo