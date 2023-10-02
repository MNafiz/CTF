import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
file = open("collected_data_3b1eecad8d7b9a4e92b93efcdbf8113b.txt", "r")
data = json.loads(file.read())
for k in range(100, 200):
    dic = {}
    for i in range(len(data[0])):
        dic[i] = [0, 0]

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] > k:
                dic[j][1] += 1
            else:
                dic[j][0] += 1
    flag2 = ""
    for i in range(len(dic)):
        if dic[i][1] > dic[i][0]:
            flag2 = "1" + flag2
        else:
            flag2 = "0" + flag2
    flag = long_to_bytes(int(flag2, 2))
    if b'crypto' in flag:
        print(flag)
        break