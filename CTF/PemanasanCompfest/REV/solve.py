from pwn import *
from itertools import permutations
from random import choices

# r = process("./soal")

NC = "nc 34.101.174.85 10003".split()
r = remote(NC[1],NC[2])

# payload = cyclic(20).decode().upper()
# payload = list(payload)

# for i in range(4,24,5):
#     payload[i] = "-"

# print("".join(payload))

# list_udah = []
# LIST_CHAR = "ABCDE"
# list_acak = list(permutations(LIST_CHAR,r=4))

# sukses = 0
# while True:
#     pilih_acak = choices(list_acak,k=5)
#     for i in range(5):
#         pilih_acak[i] = "".join(pilih_acak[i])

#     payload = "-".join(pilih_acak)

#     if payload in list_udah:
#         continue
#     list_udah.append(payload)
#     sukses += 1
#     r.sendlineafter(b"> ", payload.encode())
#     if sukses == 10:
#         break

list_char = cyclic(2000).decode()

for i in range(100):
    pilih = list_char[20*i:20*i+20].upper()
    payload = pilih[0:4] + "-" + pilih[4:8] + "-" + pilih[8:12] + "-" + pilih[12:16] + "-" + pilih[16:20]
    r.sendlineafter(b"> ", payload.encode())
flag = r.recvuntil(b"}").decode()
r.close()


log.success(f"Flag : {flag}")