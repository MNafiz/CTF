from pwn import *
from Crypto.Util.number import *

context.log_level = "warning"

dapetGa = False
cnt = 0
while True:
    cnt += 1
    print(f"percobaan ke-{cnt}")
    try:
        r = remote("ctf-gemastik.ub.ac.id", "10001")

        r.recvuntil(b"values:\n")

        for i in range(6):
            exec(r.recvline(0))


        order_modulo = modd - 1
        divisor = GCD(4,order_modulo)
        while divisor != 1:
            order_modulo //= divisor
            divisor = GCD(4,order_modulo)

        

        if pow(3,order_modulo,modd) != 1:
            r.close()
            continue
        
        print("lolos")
        d = inverse(4,order_modulo)


        hidden_val = pow(hint_2, d, modd)
        if hidden_val.bit_length()  > 1280:
            print("Masuk sini")
            hidden_val = modd - hidden_val

        rand_1_temp = hidden_val % n
        for i in range(4096,1024,-1):
            temp = n*i + rand_1_temp
            z3 = (hidden_val - temp)
            if z3 % n == 0:
                z3 //= n
                if isPrime(z3) and temp.bit_length() == (modd.bit_length() - 1013):
                    

                    z2 = hint_1 // z3**8
                    if z2:
                        if n % z2 == 0:
                            z1 = n // z2
                            d = pow(65537,-1,(z1-1)*(z2-1))
                            m = pow(c,d,n)
                            dapetGa = True
                            print(i)
                            break
        if dapetGa:
            break
    except Exception as e:
        print(e)
        r.close()

r.sendlineafter(b": ",str(m).encode())
r.interactive()