from pwn import *
from binascii import hexlify, unhexlify
from Crypto.Util.Padding import pad, unpad
import base64

import json

def get_n_block(s,n):
    return bytes.fromhex(s[(n-1)*32:(32*n)])

def split(s,n):
    return s[(n-1)*32:(32*n)]

# p = process('./chall.py')

NC = "nc 103.152.242.228 1031".split()

p = remote(NC[1], NC[2])


p.sendline(b'2')
p.sendline((b'a' * 12) + b'member356')

p.recvuntil(b'adalah : ')

payload = base64.b64decode(p.recvline().strip()).decode()
secret = json.loads(payload)['secret']

b1 = get_n_block(secret,1)
b2 = get_n_block(secret,2)
b3 = get_n_block(secret,3)
b4 = get_n_block(secret,4)

b1_new = []
flip = (b1[-2] ^ ord('6') ^ ord('7')).to_bytes(1,'big')
b1_new = b1[:-2] + flip + b1[-1:]

new_secret = ( bytes(b1_new) + b2 + b3 + b4).hex()

new_ct = json.dumps(
    {
        'secret' : new_secret,
        'is_login' : 0
    }
)

p.sendline(b'1')
p.sendline(base64.b64encode(new_ct.encode()))

p.sendline(b'2')
p.recvuntil(b'? ')
p.sendline(b'malam')
p.recvuntil(b'? ')
p.sendline(b'biora')
p.recvuntil(b'? ')
p.sendline(b'5')
p.recvuntil(b'? ')
p.sendline(b'aaaaa')
p.recvuntil(b'? ')
p.recvuntil(b'kamu : ')

template = p.recvline().strip().decode()

p.sendline(b'2')
p.recvuntil(b'? ')
p.sendline(b'malam')
p.recvuntil(b'? ')
p.sendline(b'biora')
p.recvuntil(b'? ')
p.sendline(b'5')
p.recvuntil(b'? ')
p.sendline(b'aaaaasubuh')
p.recvuntil(b'? ')
p.recvuntil(b'kamu : ')

cut = p.recvline().strip().decode()

tp1 = split(template,1)
tp2 = split(template,2)
tp3 = split(template,3)
tp4 = split(template,4)
tp5 = split(template,5)

cut1 = split(cut,1)
cut2 = split(cut,2)
cut3 = split(cut,3)
cut4 = split(cut,4)
cut5 = split(cut,5)

new_kupon = tp1 + tp2 + cut2 + cut4 + cut5

"""
bitflip :
{username=aaaaaa
aaaaaamember356;
get_kupon=0;is_m
ember=1}88888888

Cut and paste :

{"pesan": "aaaaa
", "golongan": "
malam", "produk"
: "biora", "rati
ng": 5}aaaaaaaaa

{"pesan": "aaaaa
subuh", "golonga
n": "malam", "pr
oduk": "biora", 
"rating": 5}aaaa

{"pesan": "aaaaa
", "golongan": "
subuh", "produk"
: "biora", "rati
ng": 5}aaaaaaaaa
"""
p.recvuntil(b'? ')
p.sendline(b'1')
p.recvuntil(b'kamu : ')
p.sendline(new_kupon)
p.sendline(b'3')

warning(f'flip block 1 : {b1}')
warning(f'flip block 2 : {b2}')
warning(f'flip block 3 : {b3}')
warning(f'flip block 4 : {b4}')

warning(f'\n')
warning(f'payload    : {payload}')
warning(f'secret     : {secret}')
warning(f'new secret : {new_secret}')
warning(f'new CT     : {base64.b64encode(new_ct.encode()).decode()}')

warning(f'\n')
warning(f'Template 1 : {tp1}')
warning(f'Template 2 : {tp2}')
warning(f'Template 3 : {tp3}')
warning(f'Template 4 : {tp4}')
warning(f'Template 5 : {tp5}')

warning(f'\n')
warning(f'Cut 1      : {cut1}')
warning(f'Cut 2      : {cut2}')
warning(f'Cut 3      : {cut3}')
warning(f'Cut 4      : {cut4}')
warning(f'Cut 5      : {cut5}')

warning(f'\n')
warning(f'template   : {template}')
warning(f'cut        : {cut}')
warning(f'new kupon  : {new_kupon}')
p.interactive()