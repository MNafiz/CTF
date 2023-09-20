#!/usr/bin/python3

import time, random, string, numpy as np
from Crypto.Util.number import *

alphanumeric = string.ascii_uppercase + string.ascii_lowercase + string.digits
e = 0x10001

def padding(pt,size):
    res_size = size - len(pt)
    right_size = res_size//2
    left_size = res_size - right_size
    result = bytes(random.choices(range(0,255),k=left_size)) + pt + bytes(random.choices(range(0,255),k=right_size))
    return result

def gen_pub_key(BIT_SIZE):
    p = getPrime(BIT_SIZE)
    q = getPrime(BIT_SIZE)
    n = p*q
    return n,[p,q]

def encrypt_RSA(pt,BIT_SIZE):
    m = bytes_to_long(pt)
    n,factors = gen_pub_key(BIT_SIZE)
    c = pow(m,e,n)
    coefs = [random.randint(-(1<<8), 1<<8) for _ in range(2)]
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
    break
    if guess != answer or (end-start) > 1:
        print("Gagal")
        exit(0)

finalAnswer = "".join(random.choices(alphanumeric,k=30))
finalAnswerFormat = "answer{" + finalAnswer + "}"
finalAnswerPad = padding(finalAnswerFormat.encode(),dim)
finalAnswerVector = [i for i in finalAnswerPad]

Vektor = np.dot(mat,finalAnswerVector)

print(f"{Vektor = }")

start = time.time()
guess = input("What's the final answer? ")
end = time.time()

if guess == finalAnswer:
    print(f"Flag : {finalAnswerFormat}")
else:
    print("Yah dikit lagii")

print(end-start)