from pwn import *
from Crypto.Util.number import *
from math import gcd
import time
from itertools import product

r = process(['python3', 'server.py'])

ans = lambda x: r.sendlineafter(b'What\'s the secret? ', f'{x}'.encode())
e = 0x10001
batas = 50
number_list =  list(range(1,batas+1))

list_product = [i*j for i, j in list(product(number_list,repeat=2))]
list_product = list(set(list_product))

print(len(list_product))

for loop in range(10):
    start = time.time()
    for _ in range(4):
        exec(r.recvline(0))

    finish = False  
    for i in list_product:
        print(i)
        for j in list_product:
            try:
                # inv1 = pow(i, -1, n)
                # inv2 = pow(j, -1, n)
                hint1 = (hint_1 * i) % n
                hint2 = (hint_2 * j) % n
                hint = hint1 - hint2
                if hint == 0:
                    continue
                if (p:= gcd(hint%n,n)) != 1:
                    q = n // p 
                    d = pow(e, -1, (p-1)*(q-1))
                    guess = pow(c,d,n)
                    ans(guess)
                    finish = True
                    end = time.time()
                    print(end - start)
                    r.recvuntil(b"Good Job!\n")
                    break
                hint = hint1 + hint2
                if hint == 0:
                    continue
                if (p:= gcd(hint%n,n)) != 1:
                    q = n // p 
                    d = pow(e, -1, (p-1)*(q-1))
                    guess = pow(c,d,n)
                    ans(guess)
                    finish = True
                    end = time.time()
                    print(end - start)
                    r.recvuntil(b"Good Job!\n")
                    break
            except Exception as e:
                print(e) 
                pass
        if finish:
            break
        
