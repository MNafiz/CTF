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

def get_error_msg():
    p.recvuntil(b"terdapat error pada data : ")
    result = p.recvline(0).decode()
    return bytes.fromhex(result)

pt_tujuan = b"""{"username": "nafiz", "password": "4ae71336e44bf9bf79d2752e234818a5", "saldo": "9e900"}\t\t\t\t\t\t\t\t\t"""
pt_awal = b"""{"username": "nafiz", "password": "4ae71336e44bf9bf79d2752e234818a5", "saldo": "0.000"}\t\t\t\t\t\t\t\t\t"""
pt_awal_list = [pt_awal[i:i+16] for i in range(0,len(pt_awal),16)]
pt_tujuan_list = [pt_tujuan[i:i+16] for i in range(0,len(pt_tujuan),16)]
n = len(pt_tujuan_list)

# print(pt,len(pt))


password = b"\x00"*16
iv,token = registration(b"nafiz", password)
login(iv+token)
goto(4)

for k in range(1,n):
    token = [token[i:i+16] for i in range(0,len(token),16)]
    token[-k-1] = xor(token[-k-1],pt_awal_list[-k],pt_tujuan_list[-k])
    token = b"".join(token)
    login(iv+token)
    leak = get_error_msg()
    print(leak)
    pt_awal_list = pad(leak,16)
    pt_awal_list = [pt_awal_list[i:i+16] for i in range(0,len(pt_awal_list),16)]

iv = xor(iv,pt_awal_list[-n],pt_tujuan_list[-n])

login(iv+token)

for i in range(2):
    goto(3)

# print(get_error_msg())

p.interactive()

