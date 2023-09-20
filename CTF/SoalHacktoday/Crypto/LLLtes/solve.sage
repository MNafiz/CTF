from sage.all import *
from Crypto.Util.number import *
from Crypto.Util.Padding import unpad
from gmpy2 import *
from itertools import product
from Crypto.Cipher import AES
import hashlib

with open("output.txt","r") as f:
    exec(f.read())
    f.close()

def decryptFlag(plain: bytes, key: int):
    IV = plain[:16]
    cipher = AES.new(hashlib.sha256(str(key).encode()).digest()[:16], AES.MODE_CBC, iv=IV)
    return cipher.decrypt(plain[16:])

batas = 1000
number_list = list(range(1,batas+1))

list_product = [i*j for i, j in list(product(number_list,repeat=2))]
list_product = list(set(list_product))

print(len(list_product))

hint_1_quad = hint_1**2
for prod in list_product:
    temp = iroot(hint_1_quad + 4 * prod * n, 2)
    if temp[1]:
        print("Found")
        hint_2 = int(temp[0])
        p = GCD(hint_1 + hint_2, n)
        q = n // p
        d = pow(65537, -1 , (p-1)*(q-1))
        koefs_1 = pow(enc_pub_1,d,n)
        break

list_pub = [koefs_1] + list_pub



for power in range(256,257):
    sv = 2**power
    mat = Matrix(ZZ,[
        [sv,0,0, list_pub[0]],
        [0,sv,0, list_pub[1]],
        [0,0,sv, list_pub[2]],
        [0,0,0, -S]
    ])

    # mat = Matrix(ZZ,[
    #     [list_pub[0],sv,0,0],
    #     [list_pub[1], 0,sv,0],
    #     [list_pub[2],0,0,sv],
    #     [-S, 0,0,0]
    # ])


    mat = mat.LLL()

    for j in range(4):
        try:
            list_d = list(mat[j])

            flag = b""
            for i in range(4):
                key = list_d[i]
                if i != 3:
                    key //= sv
                plain = bytes.fromhex(LIST_ENC_FLAG[i])
                # print(key)
                flag += unpad(decryptFlag(plain,key),16)

            print(flag.decode(), len(flag), j, power)
        except:
            continue
