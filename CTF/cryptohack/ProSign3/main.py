from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192, curve_192
from ecdsa import ellipticcurve
from pwn import *
import json
import hashlib
from Crypto.Util.number import *
import time


def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()


g = generator_192
n = g.order()
msg = "unlock"
hsh = bytes_to_long(sha1(msg.encode()))
_p = 6277101735386680763835789423207666416083908700390324961279
_b = int("64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1", 16)
_a = -3
_r = 6277101735386680763835789423176059013767194773182842284081

rem = remote("socket.cryptohack.org", 13381)
print(rem.recvline())

send = {'option': 'sign_time'}
send = json.dumps(send).encode()
gse_arr = []

rem.sendline(send)
data = json.loads(rem.recvline().decode())
print(data)
m = data["msg"]
h = bytes_to_long(sha1(m.encode()))
r = int(data["r"], 16)
s = int(data["s"], 16)
print(s, r, h)

y_2 = (r ** 3 - 3 * r + _b) % _p
y_arr = []
y = pow(y_2, (_p + 1) >> 2, _p)
y_arr.append(y)
y_arr.append(_p - y)
for y in y_arr:
    g_k = ellipticcurve.PointJacobi(curve_192, r, y, 1, _r, generator=True)
    g_ks = s * g_k
    inv_r = inverse(r, n)
    g_se = inv_r * (g_ks + ((0 - h) % n) * g)
    gse_arr.append(g_se)

rem.sendline(send)
data = json.loads(rem.recvline().decode())
print(data)
m = data["msg"]
h = bytes_to_long(sha1(m.encode()))
r = int(data["r"], 16)
s = int(data["s"], 16)
print(s, r, h)

y_2 = (r ** 3 - 3 * r + _b) % _p
y_arr = []
y = pow(y_2, (_p + 1) >> 2, _p)
    y_arr.append(y)
y_arr.append(_p - y)
for y in y_arr:
    g_k = ellipticcurve.PointJacobi(curve_192, r, y, 1, _r, generator=True)
    g_ks = s * g_k
    inv_r = inverse(r, n)
    g_se = inv_r * (g_ks + ((0 - h) % n) * g)
    gse_arr.append(g_se)
for i in range(len(gse_arr) - 1):
    for j in range(i + 1, len(gse_arr)):
        if gse_arr[i].x() == gse_arr[j].x():
            print("oke")
            g_se = gse_arr[i]
print(g_se.x(), g_se.y())
# print("start")
# for i in range(60):
#     current = f"7:{i}"
#     if bytes_to_long(sha1(f"Current time is {current}".encode())) == hsh:
#         print(i)
r_i = (hsh * r) * inverse(h, n) % _r
g_k = inverse(s, n) * (h * g + r * g_se)
s_arr = []
h_arr = []
for i in range(60):
    rem.sendline(send)
    data = json.loads(rem.recvline().decode())
    print(data)
    if data['r'] == r:
        print("oke 2")
        r = int(r, 16)
        s_arr.append(int(s, 16))
        s_arr.append(int(data['s'], 16))
        h_arr.append(bytes_to_long(sha1(m.encode())))
        h_arr.append(bytes_to_long(sha1(data['msg'].encode())))
        break
    else:
        r = data['r']
        s = data['s']
        m = data['msg']
    if int(data['msg'].split('Current time is 7:')[1]) == 58 or int(data['msg'].split('Current time is 7:')[1]) == 59:
        time.sleep(3)
secret = (s_arr[0] * h_arr[1] - h_arr[0] * s_arr[1]) * inverse(r * (s_arr[1] - s_arr[0]), _r) % _r
secret = _r - secret

k = inverse(int(s, 16), _r) * (bytes_to_long(sha1(m.encode())) + secret * r) % _r
s_i = inverse(k, _r) * (hsh + secret * r) % _r
send = {'option': 'verify', 'msg': msg, 'r': hex(r), 's': hex(s_i)}
send = json.dumps(send).encode()
rem.sendline(send)

print(rem.recvline())