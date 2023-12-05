from PIL import Image
import numpy as np
from Crypto.Util.number import *

def rescale(arr):
    mod = len(arr)
    final_arr = np.zeros(shape=(mod*10,mod*10), dtype=bool)
    for i in range(mod):
        for j in range(mod):
            final_arr[i*10:(i+1)*10, j*10:(j+1)*10] = arr[i][j]

    return final_arr

a = np.array(Image.open("hehe.png"))

a = rescale(a)

a = Image.fromarray(a)
a.save("hehe.png")