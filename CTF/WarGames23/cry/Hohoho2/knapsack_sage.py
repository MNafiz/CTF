from Crypto.Cipher import AES
from Crypto.Util.number import *
import hashlib

Ciphertext = "af95a58f4fbab33cd98f2bfcdcd19a101c04232ac6e8f7e9b705b942be9707b66ac0e62ed38f14046d1cd86b133ebda9"

choices =  [600848253359, 617370603129, 506919465064, 218995773533, 831016169202, 501743312177, 15915022145, 902217876313, 16106924577, 339484425400, 372255158657, 612977795139, 755932592051, 188931588244, 266379866558, 661628157071, 428027838199, 929094803770, 917715204448, 103431741147, 549163664804, 398306592361, 442876575930, 641158284784, 492384131229, 524027495955, 232203211652, 213223394430, 322608432478, 721091079509, 518513918024, 397397503488, 62846154328, 725196249396, 443022485079, 547194537747, 348150826751, 522851553238, 421636467374, 12712949979]
target =  7929089016814


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
        print("dapet")
        sol = subsetKiri[jumlah] + subsetKanan[jumlah]
        break

print("selesai", sol)

sol = long_to_bytes(int(sol[::-1], 2))
print(len(sol))
#sol = b"The seccret has been " + sol
key = hashlib.sha256(sol).digest()[:16]

cipher =  AES.new(key, AES.MODE_ECB)

print(cipher.decrypt(bytes.fromhex(Ciphertext)))
