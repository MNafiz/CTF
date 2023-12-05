from PIL import Image
import numpy as np
import qrcode

def rescale(arr):
    mod = len(arr)
    final_arr = np.zeros(shape=(mod*10,mod*10), dtype=bool)
    for i in range(mod):
        for j in range(mod):
            final_arr[i*10:(i+1)*10, j*10:(j+1)*10] = arr[i][j]

    return final_arr

FLAG = open('flag.txt', 'r').read()

qr = qrcode.QRCode(border=0)
qr.add_data(FLAG)
qr.make(fit=True)

mat = np.array(qr.get_matrix(), dtype=bool)

mat = rescale(mat)

img = Image.fromarray(mat)
img.save('tes.png')

