import random
from randcrack import RandCrack

rc = RandCrack()

def wow():
    wiw = [random.getrandbits(32) for i in range(4)]
    wow = [wiw[i] << (128*pow(2,i)) for i in range(0, 4)]
    wadidaw = 0
    for i in wow:
        wadidaw |= i
    return wadidaw, wow, wiw

# res1, res2, res3 = wow()
# res2 = [res2[i] >> (128*pow(2,i)) for i in range(0, 4)]

# hasil = []
# print(res1)

# mask = 128

for j in range(156):
    print(j+1)
    res1, res2, res3 = wow()
    mask = 128
    for i in range(4):
        res1_temp = res1 >> mask
        rc.submit(res1_temp % (1 << 32))
        mask *= 2

print(rc.predict_getrandbits(32))
print(rc.predict_getrandbits(32))
print(rc.predict_getrandbits(32))
print(rc.predict_getrandbits(32))
print(wow())

