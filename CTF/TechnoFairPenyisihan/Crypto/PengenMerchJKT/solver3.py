from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import json,hashlib

p = process("./server.py")

# p = remote("103.152.242.197", 54223)

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

def login(token,getFlag=False):
    goto(1)
    p.sendlineafter(b": ", token.hex().encode())
    if getFlag:
        for i in range(2): goto(3)
        p.recvuntil(b"yaudah ni ")
        return p.recvline(0).decode()

def get_error_msg():
    p.recvuntil(b"terdapat error pada data : ")
    result = p.recvline(0).decode()
    return bytes.fromhex(result)


pt_tujuan = b"""{"username": "nafiz", "password": "4ae71336e44bf9bf79d2752e234818a5", "saldo": "9999999999"}"""
pt_tujuan = pad(pt_tujuan,16)
pt_awal = b"""{"username": "nafiz", "password": "4ae71336e44bf9bf79d2752e234818a5", "saldo": "0.000"}\t\t\t\t\t\t\t\t\t"""
pt_awal_list = [pt_awal[i:i+16] for i in range(0,len(pt_awal),16)]
pt_tujuan_list = [pt_tujuan[i:i+16] for i in range(0,len(pt_tujuan),16)]
n = len(pt_tujuan_list)
log.info("Preparing payload for byte flipping value of saldo to 999.999.999")


password = b"\x00"*16
iv,token = registration(b"nafiz", password)
log.info("regist account to get iv and token")


for k in range(1,n):
    token = [token[i:i+16] for i in range(0,len(token),16)]
    token[-k-1] = xor(token[-k-1],pt_awal_list[-k],pt_tujuan_list[-k])
    token = b"".join(token)
    login(iv+token)
    leak = get_error_msg()
    pt_awal_list = pad(leak,16)
    pt_awal_list = [pt_awal_list[i:i+16] for i in range(0,len(pt_awal_list),16)]
log.info("byte flipping second block until last block from the token")


iv = xor(iv,pt_awal_list[-n],pt_tujuan_list[-n])
log.info("byte flipping first block from the token")

flag = login(iv+token,getFlag=True)
log.info("Got the flag !!!")


log.success(flag)

p.interactive()

