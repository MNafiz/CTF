#!/usr/bin/python3

from secret import key
from hashlib import sha256
from sys import argv, exit

def bxor(dest: bytes, src: bytes):
    ret = []
    ls = len(src)
    for i in range(len(dest)):
        ret.append(dest[i] ^ src[i % ls])
    return bytes(ret)

if __name__ == '__main__':

    if len(argv) == 1:
        print(f'Usage {argv[0]} <file-to-sign>')
        exit(1)
    with open(argv[1], 'rb') as f:
        data = f.read()
        data += bxor(sha256(data).digest(), key)
    with open(argv[1]+'.sign', 'wb') as f:
        f.write(data)
