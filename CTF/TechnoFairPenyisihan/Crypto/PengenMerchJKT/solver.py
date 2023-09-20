from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import json,hashlib

#p = remote("103.152.242.197", 54223)

p = process("./server.py")

def goto(n):
    p.sendlineafter(b"$ ", str(n).encode())

def registration(username,password):
    goto(2)
    p.sendlineafter(b": ", username)
    p.sendlineafter(b": ", password)
    p.recvuntil(b"token: ")
    result = bytes.fromhex(p.recvline(0).decode())
    iv = result[:16]
    token = result[16:]
    return iv,token

def login(token):
    goto(1)
    p.sendlineafter(b": ", token.hex().encode())

pt = b"""{"username": "nafiz", "password": "4ae71336e44bf9bf79d2752e234818a5", "saldo": "0.000"}\t\t\t\t\t\t\t\t\t"""

print(pt,len(pt))


password = b"\x00"*16
iv,token = registration(b"nafiz", password)
login(iv+token)

# pt = [pt[i:i+16] for i in range(0,len(pt),16)]
# token = [token[i:i+16] for i in range(0,len(token),16)]


# # print(token[-2])
# # print(pt[-1])

# print(pt)
# print(token)

# # login(iv+token)

# # print(pt,token)

# pengganti_token_block_akhir = xor(pt[-1],token[-2])
# pengganti_token_block_akhir = list(pengganti_token_block_akhir)
# pengganti_token_block_akhir[0] ^= (ord("0") ^ ord("9"))
# pengganti_token_block_akhir[1] ^= (ord(".") ^ ord("e"))
# pengganti_token_block_akhir[2] ^= (ord("0") ^ ord("9"))



# token = b"".join(token)
# token = token[-48:-32] + bytes(pengganti_token_block_akhir) + token[-16:]

# #goto(4)

# # print(len(token))
# login(iv+token)



p.interactive()

