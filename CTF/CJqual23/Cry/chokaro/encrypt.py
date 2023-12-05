import random
import numpy as np
import qrcode
from PIL import Image

def mix(a,b,arr):
    mod = len(arr)
    narr = np.zeros(shape=(mod,mod), dtype=bool)
    for (x,y), element in np.ndenumerate(arr):

        ny = (y - b * x) % mod
        nx = (x - ny * a)
        # nx = (x + y * a) % mod
        # ny = (x * b + y * (a * b + 1)) % mod

        narr[nx][ny] = element

    return narr
    

def inverse_rescale(arr):
    mod = arr.shape[0] // 10
    original_arr = np.zeros(shape=(mod, mod), dtype=bool)
    for i in range(mod):
        for j in range(mod):
            original_arr[i, j] = np.any(arr[i*10:(i+1)*10, j*10:(j+1)*10])

    return original_arr

FLAG = open('flag.txt', 'r').read()

qr = qrcode.QRCode(border=0)
qr.add_data(FLAG)
qr.make(fit=True)

mat = np.array(qr.get_matrix(), dtype=bool)

a = random.randrange(1, len(mat)-1)
b = random.randrange(1, len(mat)-1)

scrambled = mat
for _ in range(22):
    scrambled = mix(a,b,scrambled)

scrambled = rescale(scrambled)

img = Image.fromarray(scrambled)
img.save('mixed.png')