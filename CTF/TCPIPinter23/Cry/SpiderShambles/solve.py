from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as btl
from randcrack import RandCrack
import requests

rc = RandCrack()

# with open("payload.jpeg", "wb") as f:
#     f.write(b"\x00"*2496)
#     f.close()

url = "http://ctf.tcp1p.com:54734/"

payload = open("payload.jpeg", "rb")

r = requests.post(url, files={"file" : payload, 'Content-Type': 'image/jpeg'})

# print(r.text, len(r.content))

print(type(r.content))
result = btl(r.content)

mask = (1 << 32) - 1
while result:
    rc.submit(result & mask)
    result >>= 32

print("selesai")

r = requests.get(url + "flago")

def xor(a, b):
    return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

n = len(r.content)

# flag = b""
# for i in range(1,n+1):
#     rand = l2b(rc.predict_getrandbits( 8))
#     flag += xor(bytes([r.content[-i]]), rand)
#     if i % 100 == 0:
#         print(i)


rand = l2b(rc.predict_getrandbits(n * 8))
flag = xor(r.content, rand)


with open("./flago.jpeg", "wb") as f:
    f.write(flag)
    f.close()
print("dapet flag")