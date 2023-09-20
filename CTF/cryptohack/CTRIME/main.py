import json
import requests
from Crypto.Cipher import DES3
import zlib
from Crypto.Util import Counter
import os
import string


def encrypt(plaintext):
    r = requests.get(f'http://aes.cryptohack.org/ctrime/encrypt/{plaintext}/')
    return json.loads(r.text)['ciphertext']


alphabet = '{' + '}' + '!' + '_' + '@' + '?' + string.ascii_uppercase + string.digits + string.ascii_lowercase

flag = b"crypto{CRIME"
while True:
    cipher = encrypt(flag.hex())
    size = len(cipher)
    for c in alphabet:
        cipher = encrypt((flag + c.encode()).hex())
        if len(cipher) == size:
            flag += c.encode()
            break
    if flag[len(flag) - 1] == b'}':
        break
    size += 2
    print(flag)
print(flag)