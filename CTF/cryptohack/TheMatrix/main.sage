from Crypto.Util.number import  long_to_bytes, inverse
from sage.all import *

P = 2
N = 50
E = 31337

FLAG = b'crypto{??????????????????????????}'

def bytes_to_binary(s):
    bin_str = ''.join(format(b, '08b') for b in s)
    bits = [int(c) for c in bin_str]
    return bits

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(P), rows)

mat = load_matrix("flag_403b981c77d39217c20390c1729b15f0.enc")
mat2 = mat^inverse(E, mat.multiplicative_order())
flag = ""
for j in range(N):
    for i in range(N):
        flag += str(mat2[i, j])
for i in range(8, len(flag), 8):
    s = long_to_bytes(int(flag[:i], 2))
    if b'}' in s:
        print(s)
        break
