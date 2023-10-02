from sage.all import *

enc =  [(6270022, 2279888, 4611000, 6865110, 7131265, 2632260), (6513518, 2104512, 4979880, 6603582, 7069254, 2909340), (7000510, 4165180, 5579310, 3399864, 6821210, 1579356), (5783030, 2323732, 5394870, 4903650, 3224572, 2632260), (5965652, 4428244, 5256540, 6865110, 6759199, 1440816), (6452644, 3200612, 5072100, 3399864, 7131265, 1357692)]
enc = Matrix(enc)

list_key = [65382,62011,60874,46110,43844,27708]

key = [
    [60874,0,0,0,0,0],
    [0,43844,0,0,0,0],
    [0,0,46110,0,0,0],
    [0,0,0,65382,0,0],
    [0,0,0,0,62011,0],
    [0,0,0,0,0,27708]
]
key = Matrix(key)

Hasil = enc*key.inverse()

flag = b""
for vec in Hasil:
    flag += bytes(vec)
print(b"TechnoFairCTF{"+flag+b"}")