import signal
from functools import reduce
from operator import mul
from math import log, e, ceil
from secrets import SystemRandom
from flag import FLAG
from Crypto.Util.number import bytes_to_long

random = SystemRandom()

def get_primes(n):

    # See https://math.stackexchange.com/questions/1270814/bounds-for-n-th-prime
    ub = ceil(n * (log(n, e) + log(log(n, e), e)))
    nums = list(range(2, ub))

    idx = 0
    while nums[idx] * nums[idx] < max(nums):
        if nums[idx] != -1:
            for i in range(nums[idx] * 2, len(nums), nums[idx]):
                nums[i - 2] = -1
        idx += 1

    return list(filter(lambda x: x != -1, nums))[:n]

primorial = lambda n: reduce(mul, get_primes(n), 1)

def el_gamal_gen_key():

    q = primorial(172) + 1

    g = random.randint(2, q - 1)
    x =  random.randint(1, q - 1)
    h = pow(g,x,q)

    return (q,g,h), (x)

def el_gamal_encrypt(m, pubkey):

    (q,g,h) = pubkey

    assert(bytes_to_long(m) < q)

    y =  random.randint(1, q-1)
    s = pow(h, y, q)
    c1 = pow(g,y,q)
    c2 = (bytes_to_long(m) * s) % q

    return (c1,c2)



if __name__ == '__main__':
    pubkey, privkey = el_gamal_gen_key()
    print("ct: ", el_gamal_encrypt(FLAG, pubkey))
    print("pubkey: ", pubkey)

