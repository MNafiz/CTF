from Crypto.Util.number import bytes_to_long, long_to_bytes

# SECRET_T = [?, ?, ?, ?]
FLAG = b"crypto{????????????????????????????????????????}"
size = 48

file = open("output_7e5c4d93fa5d065d105e32efd7ef9682.txt", "r")
data = file.read()[:-1]
file.close()
a = []
b = []
start = 3
for i in range(start, start + 384):
    n_a = []
    for j in range(384):
        if data[i + j] == '0':
            n = 0
        else:
            n = 1
        n_a.append(n)
    a.append(n_a)
    if data[i + 384] == '0':
        b.append(0)
    else:
        b.append(1)

for j in range(len(a) - 1):
    c = []
    for m in range(384):
        count = 0
        for n in range(384):
            if a[m][n] == 1:
                break
            else:
                count += 1
        c.append(count)
    for m in range(j, 383):
        for n in range(m + 1, 384):
            if c[m] > c[n]:
                a[m], a[n] = a[n], a[m]
                b[m], b[n] = b[n], b[m]
                c[m], c[n] = c[n], c[m]
    h = j
    while h < 384 and a[j][h] == 0:
        h += 1
    if h == 384:
        break
    for i in range(j + 1, len(a)):
        if a[i][h] == 0:
            continue
        else:
            for k in range(h, len(a)):
                a[i][k] = (a[i][k] - a[j][k]) % 2
            b[i] = (b[i] - b[j]) % 2

c = []
for m in range(384):
    count = 0
    for n in range(384):
        if a[m][n] == 1:
            break
        else:
            count += 1
    c.append(count)
x = [0 for _ in range(384)]
for i in range(383, -1, -1):
    s = 0
    for j in range(i + 1, 384):
        s += a[i][j] * x[j]
    x[i] = (b[i] - s) % 2
SECRET_T = []
for i in range(len(x)):
    if x[i] == 1:
        SECRET_T.append(i)
print(SECRET_T)
for _ in range(16 * 48):
    n = int(data[383], 2) ^ 0
    for t in SECRET_T:
        if t == 0:
            continue
        else:
            n ^= int(data[t - 1], 2)
    data = str(n) + data
print(long_to_bytes(int(data, 2)))