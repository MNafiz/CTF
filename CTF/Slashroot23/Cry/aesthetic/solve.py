from pwn import *
from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES
import base64, json

import os

IV = os.urandom(16)
KEY = os.urandom(16)


NC = "nc 103.152.242.228 1031".split()

r = remote(NC[1], NC[2])

# r = process("./chall.py")

def goto(n):
    r.sendlineafter(b"choise : ", str(n).encode())

def register(username):
    goto(2)
    r.sendlineafter(b"kamu : ", username)
    r.recvuntil(b"Session kamu adalah : ")
    return r.recvline(0)

def login(session):
    goto(1)
    r.sendlineafter(b"session kamu : ", session)

def get_kupon(msg):
    r.sendlineafter(b"? ", b"2")
    r.sendlineafter(b"? ", b"pagi")
    r.sendlineafter(b"? ", b"biora")
    r.sendlineafter(b"? ", b"5")
    # msg = b'a'*5 + pad(b'{username="amember37";get_kupon=1;is_member=1}',16) 
    r.sendlineafter(b"? ", msg)
    r.recvuntil(b"kamu : ")
    return r.recvline(0)

session = register(b"amember357")
payload = json.loads(base64.b64decode(session))
print(payload)
payload["is_login"] = 0
secret = payload["secret"]
session = base64.b64encode(json.dumps(payload).encode())

print(session)
login(session)
inject_dict = pad(b'{"aaa" : 1, "golongan" : "subuh", "rating" : 5}', 16)

panjang_plod = len(inject_dict)
msg = b'a'*5 + inject_dict
kupon = get_kupon(msg)
print(kupon, len(kupon), panjang_plod)
new_kupon = kupon[32:(32+2*panjang_plod)]
print(new_kupon)

# print(kupon, len(kupon))
# baru = kupon[16:16+len(secret)]
# print(secret, baru)
# print(len(secret), len(baru))

print(inject_dict)
print(unpad(inject_dict,16))
print(json.loads(unpad(inject_dict,16))['rating'])

def gen(golongan, produk, rating, pesan):
    review = {'pesan' : pesan, 'golongan' : golongan, 'produk':produk, 'rating' : rating}
    cipher = AES.new(KEY, AES.MODE_ECB)
    enc = cipher.encrypt(pad(json.dumps(review).encode(),16))
    return enc.hex()

def verify(kupon):
    read = bytes.fromhex(kupon)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.decrypt(read)


huhu = gen("malam", "biora", 5, "aaaaa{''golongan'' : ''subuh''}, ''rating'' : 5}")
print(huhu)
new_huhu = huhu[32:128]
print(verify(new_huhu)[:2])


r.interactive()