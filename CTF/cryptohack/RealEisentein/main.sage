import math
from decimal import *
import numpy
from sage.all import *

getcontext().prec = int(100)

FLAG = "crypto{???????????????}"
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]

ciphertext = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433

keys = []
for p in PRIMES:
    keys.append(Decimal(int(p)).sqrt())

arr = []
for k in keys:
    arr.append(int(k * int(16) ** int(64)))


def encrypt(res):
    h = Decimal(int(0))
    for i in range(len(keys)):
        h += res[i] * keys[i]
    ct = int(h * int(16) ** int(64))
    return ct


def f(N):
    size = len(arr)
    A = Matrix(ZZ, size + 1, size + 1)
    for i in range(size):
        A[i, i] = 1
        A[i, size] = arr[i] // N
        A[size, i] = 64

    A[size, size] = ciphertext // N
    res = A.LLL()

    for i in range(size + 1):
        flag = True
        for j in range(size):
            if -64 <= res[i][j] < 64:
                continue
            flag = FLAG
            break
        if flag:
            vec = [int(v + 64) for v in res[i][:-1]]
            ret = encrypt(vec)
            if ret == ciphertext:
                print(N, bytes(vec))


for i in range(1, 10):
    f(i)