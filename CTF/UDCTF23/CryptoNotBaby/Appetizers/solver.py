from math import log

choices = [19728964, 30673077, 137289540, 195938621, 207242611, 237735979, 298141799, 302597011, 387047012, 405520686, 424852916, 461998372, 463977415, 528505766, 557896298, 603269308, 613528675, 621228168, 654758801, 670668388, 741571487, 753993381, 763314787, 770263388, 806543382, 864409584, 875042623, 875651556, 918697500, 946831967]
target = 7627676296

n = len(choices) // 2
N = 2**n
subsetKiri = dict()

for i in range(1, N):
    biner = bin(i)[2:].zfill(n)
    jumlah = sum([choices[j]*int(biner[j]) for j in range(n)])
    subsetKiri[jumlah] = biner

subsetKanan = dict()

for i in range(1, N):
    biner = bin(i)[2:].zfill(n)
    jumlah = target - sum([choices[n+j]*int(biner[j]) for j in range(n)])
    subsetKanan[jumlah] = biner
    if jumlah in subsetKiri:
        sol = subsetKiri[jumlah] + subsetKanan[jumlah]
        break

print("selesai", sol)

sol = [int(i) for i in sol]
flag = [choices[i] for i in range(len(choices)) if sol[i]]
flag = "UDCTF{" + "_".join(map(str,flag)) + "}"
print(flag, 30 / log(max(choices), 2))
print(max(choices))