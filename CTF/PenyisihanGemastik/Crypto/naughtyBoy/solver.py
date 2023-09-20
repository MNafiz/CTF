from pwn import *
from Crypto.Util.number import *

while True:
    r = remote("ctf-gemastik.ub.ac.id", "10001")

    r.recvuntil(b"values:\n")

    for i in range(6):
        exec(r.recvline(0))



    divisor = GCD(4,modd-1)
    if pow(3,(modd-1)//divisor,modd) != 1:
        r.close()
        continue
    
    d = inverse(4,(modd-1)//divisor)


    hidden_val = pow(hint_2,d,modd)


    rand_1_temp = hidden_val % n
    for i in range(1000,4000):
        temp = n*i + rand_1_temp
        z3 = (hidden_val - temp)
        if z3 % n == 0:
            z3 //= n
            if hidden_val == (n*z3) + temp and isPrime(z3):
                print("dapet",i)
                
    r.interactive()