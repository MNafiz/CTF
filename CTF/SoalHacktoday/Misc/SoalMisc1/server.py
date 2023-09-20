#!/usr/bin/python3

import time, random, string, numpy as np
from Crypto.Util.number import *

flag = open("flag.txt","r").read()
alphanumeric = string.ascii_uppercase + string.ascii_lowercase + string.digits
e = 0x10001

def gen_pub_key(BIT_SIZE):
    p = getPrime(BIT_SIZE)
    q = getPrime(BIT_SIZE)
    n = p*q
    return n,[p,q]

def encrypt_RSA(pt,BIT_SIZE):
    m = bytes_to_long(pt)
    n,factors = gen_pub_key(BIT_SIZE)
    c = pow(m,e,n)
    coefs = random.choices(list(range(-255,0)) + list(range(1,256)) ,k=2)
    leak = sum([i*j for i,j in zip(factors,coefs)])
    return c,n,leak,coefs

for i in range(100):


    answer = "".join(random.choices(alphanumeric,k=30))
    c, n, leak, coefs = encrypt_RSA(answer.encode(),1024)
    
    print(f"{n = }")
    print(f"{c = }")
    print(f"{leak = }")
    print(f"{coefs = }")

    start = time.time()
    guess = input("What's the answer? ")
    end = time.time()
    if guess != answer or (end-start) > 1:
        print("Gagal")
        exit(0)

print(f"Congrats Here's the Flag : {flag}")