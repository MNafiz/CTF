from Crypto.Util.number import *
from random import randint, getrandbits
from libnum import xgcd

NBIT = 2048

FLAG = b"hacktoday{dummy_flag}"

def get_factor(NBIT):
    return getPrime(NBIT//2), getPrime(NBIT//2)


def main():
    m = bytes_to_long(FLAG)
    p, q = get_factor(NBIT)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = getPrime(5)
    list_e =  [e * getrandbits(2043) for _ in range(1)]
    list_d = [getPrime(32) for _ in range(9)]
    ed_sum = sum([i*j for i, j in zip(list_e,list_d)])
    last_e = phi + 1 - ed_sum
    list_e.append(last_e)
    
    print(f"{n = }")
    for i in range(10):
        e = list_e[i]
        c = pow(m,e,n)
        print(f"{e = }")
        print(f"{c = }")


if __name__ == "__main__":
    main()