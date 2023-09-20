from pwn import *
from Crypto.Util.number import *
from sage.all import *

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


    hidden_val = Zmod(modd)(hint_2)^d
    print("bsoa", hidden_val)
    hidden_val = int(hidden_val)
    print("bsoa", hidden_val)


    rand_1_temp = hidden_val % n
    for i in range(1000,4000):
        temp = n*i + rand_1_temp
        z3 = (hidden_val - temp)
        if z3 % n == 0:
            z3 //= n
            if hidden_val == (n*z3) + temp and isPrime(z3) and temp.bit_length() == (modd.bit_length() - 1013):
                print("dapet",i)
                


                print(n*z3 + temp == hidden_val)
                # scale_v = 1
                # mat = Matrix(ZZ,[
                #     [scale_v,0,0, z3**8],
                #     [0,scale_v,0, n*0x1337],
                #     [0,0,scale_v, -hint_1],
                # ])

                # mat = mat.LLL()

                # k = abs(mat[0][2] // scale_v)
                # print(k)

                # print(n)


                z2 = hint_1 // z3**8

    r.interactive()