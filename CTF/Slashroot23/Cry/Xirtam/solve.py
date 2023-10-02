# from sage.all import *
from Crypto.Util.Padding import unpad

def pad(text):
    padding_len = 16 - (len(text) % 16)
    return text + bytes([padding_len]) * padding_len

def xor(a, b):
    return [ord(x)^y for x,y in zip(a,b)]

def t2m(s,r,c):
    if len(s) != (r * c):
        print("Incorect Matrix Size!")
        exit()

    ascii_values = np.zeros(len(s), dtype=int)

    for i, char in enumerate(s):
        ascii_values[i] = ord(char)

    matrix = np.reshape(ascii_values, (r, c))

    return matrix

from itertools import product
import string
possibleKey = list(product(string.ascii_uppercase, repeat=4))
# print("".join(possibleKey[0]))


cip = [8510, 8278, 8336, 7945, 8130, 7850, 10758, 11289, 8574, 8159, 8048, 7619, 8520, 8255, 7820, 7579, 8233, 7948, 12761, 11643, 8349, 8068, 12361, 11123, 8574, 8159, 11745, 12109, 8375, 8097, 15727, 15237, 8430, 8158, 12493, 11187, 8065, 7900, 8066, 8005, 8505, 8205, 10925, 11433, 8520, 8255, 8237, 7809, 8569, 8068, 10760, 11269, 8485, 8264, 8022, 7753, 7955, 7857, 11081, 11625, 8023, 7825, 7793, 7593, 7930, 7666, 7433, 7191, 8546, 8090, 15520, 14981, 7825, 7785, 8279, 7941, 7770, 7615, 11591, 12033, 7830, 7730, 8135, 7727, 7821, 7724, 8192, 7997, 7894, 7739, 11396, 11959, 7770, 7615, 11591, 12033]
cip = [cip[i:i+16] for i in range(0, len(cip), 16)]
result = []
IV = list(pad("slashroot7{".encode('latin1')).decode())

for i in range(len(cip) - 1, -1, -1):
    cip[i] = xor(IV, cip[i])

cip = [j for i in cip for j in i]
cip = [cip[i:i+2] for i in range(0, len(cip), 2)]
import numpy as np
cipM = np.array(cip, dtype=int)

#print(cipM)

iterasi = 0
for K in possibleKey:
    iterasi += 1
    KEY = "".join(K)
    KEY = t2m(KEY, 2, 2)
    if np.linalg.det(KEY) == 0:
        continue
    hasil = np.dot(cipM, np.linalg.inv(KEY))
    hasil = hasil.T
    hasil = [j for i in hasil for j in i]
    hasil = [round(i) for i in hasil]
    if (all(0 <= x <= 128 for x in hasil)):
        try:
            hasil = bytes(hasil)
            hasil = bytes.fromhex(hasil.decode())
            if b"slashroot" in hasil:
                print(iterasi, "Dapet", "".join(K))
                print(unpad(hasil, 16).decode())
                break
        except:
            pass
    if iterasi == 30000:
        break  

# hihi = np.array([
#     [ord("s"), ord("l")],
#     [ord("a"), ord("s")]
# ], dtype=int)