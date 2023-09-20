from Crypto.Util.number import long_to_bytes

with open("result.txt","r") as f:
    cipher = f.read().rstrip()


charset = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
cipher = cipher[:-2]
cipher2 = ""

for i in cipher:
    dec = bin(charset.index(i))[2:].zfill(5)
    cipher2 += dec

print(cipher2)
print(long_to_bytes(int(cipher2,2)>>4))


