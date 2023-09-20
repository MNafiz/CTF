from Crypto.Util.number import *
from pwn import *
import time

r = process("./server.py")

for l in range(10):
    r.recvuntil(b"flag\n")

    for i in range(5):
        exec(r.recvline(0))

    start = time.time()

    x %= n
    y %= n


    dapet = False
    for a in range(1,10):
        for b in range(1,10):
            temp_x = (x*a) % n
            temp_y = (y*b) % n
            if GCD(temp_x + temp_y,n) > 1:
                p = GCD(temp_x + temp_y,n)
                q = n//p
                d = pow(e,-1,(p-1)*(q-1))
                dapet = True
            elif GCD(temp_x - temp_y, n) > 1:
                p = GCD(temp_x - temp_y,n)
                q = n//p
                d = pow(e,-1,(p-1)*(q-1))
                dapet = True
            if dapet:
                break
        if dapet:
            break


    guess = pow(c,d,n)

    
    end = time.time()

    print(l)

    r.sendlineafter(b": ", str(guess).encode())

r.recvuntil(b"Congrats\n")

flag = r.recvline(0).decode()

log.success(f"Here's the flag : {flag}")

r.close()