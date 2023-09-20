import re
import string
import numpy as np
from Crypto.Util.number import isPrime
from pwn import *
import json


def check(password):
    if not re.fullmatch(r"\w*", password, flags=re.ASCII):
        return "Password contains invalid characters."
    if not re.search(r"\d", password):
        return "Password should have at least one digit."
    if not re.search(r"[A-Z]", password):
        return "Password should have at least one upper case letter."
    if not re.search(r"[a-z]", password):
        return "Password should have at least one lower case letter."

    array = np.array(list(map(ord, password)))
    if isPrime(int(array.sum())) and isPrime(int(array.prod())):
        return True
    return f"Wrong password, sum was {array.sum()} and product was {array.prod()}"


r = remote("socket.cryptohack.org", 13400)
alpha = string.ascii_letters + string.digits + "_"
lib = []
up_lib = []
low_lib = []
digit_lib = []
for c in alpha:
    if ord(c) % 2 == 1:
        lib.append(c)
        if ord(c) < 58:
            digit_lib.append(c)
        elif ord(c) < 91:
            up_lib.append(c)
        else:
            low_lib.append(c)
print(lib)
print(low_lib)
print(up_lib)
print(digit_lib)
PRIMES = []
for i in range(540, 1340):
    if isPrime(i):
        PRIMES.append(i)
print(PRIMES)
print(r.recvline())

for c1 in low_lib:
    for c2 in up_lib:
        for c3 in digit_lib:
            for c4 in lib:
                for c5 in lib:
                    n = ord(c1) + ord(c2) + ord(c3) + ord(c4) + ord(c5)
                    n *= 2
                    for p in PRIMES:
                        num = p - n
                        if num > 121:
                            break
                        elif num < 49:
                            continue
                        if not chr(num) in lib:
                            continue
                        password = (c1 + c2 + c3 + c4 + c5) * 2 + chr(num)
                        print(password)
                        send = {"password": password}
                        send = json.dumps(send).encode()
                        r.sendline(send)

                        data = r.recvline()
                        if b'crypto' in data:
                            print(data)
                            exit(0)
