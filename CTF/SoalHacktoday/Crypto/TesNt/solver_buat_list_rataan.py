from pwn import *
from Crypto.Util.number import *
from itertools import combinations,product

with open("./data_rataan_waktu.txt","r") as f:
    exec(f.read())
    f.close()

context.log_level = "warning"

e = 0x10001
batas = 50
number_list = list(range(1,batas+1))

list_product = [i*j for i, j in list(product(number_list,repeat=2))]
list_product = list(set(list_product))

print(len(list_product))



for sample in range(100):
    list_times = []
    r = process("./server.py")

    for loop in range(10):
        start = time.time()
        dapetP = False
        for _ in range(4):
            exec(r.recvline(0))
        hint_1 %= n
        hint_2 %= n
        for u in list_product:
            for v in list_product:
                hint_1_u = (hint_1 * u) % n
                hint_2_v = (hint_2 * v) % n
                p = GCD(hint_1_u + hint_2_v, n)
                if p == 1:
                    p = GCD(hint_1_u - hint_2_v, n)
                    if p == 1:
                        continue
                dapetP = True
                break
            if dapetP:
                break
        q = n // p
        d = pow(e,-1,(p-1)*(q-1))
        secret = str(pow(c,d,n)).encode()
        r.sendlineafter(b"? ", secret)
        r.recvuntil(b"Good Job!\n")
        times_taken = time.time() - start
        list_times.append(times_taken)
        print(loop+1, times_taken)

    print()
    mean_times = sum(list_times) / 10
    #print(f"{mean_times = }")

    r.recvuntil(b"mean_times = ")
    print("mean_times =", r.recvline(0).decode())
    r.close()