from sage.all import *
from Crypto.Util.number import *

with open("output.txt","r") as f:
    content = f.read()
    f.close()



list_content = content.split("\n")[:-1]
exec(list_content[0])
list_content = list_content[1:]

list_e = []
list_c = []

for i in range(0,20,2):
    exec(list_content[i])
    exec(list_content[i+1])
    list_e.append(e)
    list_c.append(c)

scale_value = 2**128
matrix = [[0 for i in range(12)] for j in range(12)]
for i in range(10):
    matrix[i][i] = scale_value
    matrix[i][-1] = list_e[i]
matrix[-1][-2] = 1
matrix[-1][-1] = -n

mat = Matrix(ZZ, matrix)
mat = mat.LLL()
for loop in range(11):
    res = list(mat[loop])[:-1]
    if res[-1] == 1:
        print("Ada")
    res = [i // scale_value for i in res]
    sum_ed = sum([i*j for i,j in zip(list_e,res)])

    list_m = [pow(list_c[i],res[i],n) for i in range(10)]
    m_plain = 1
    for m in list_m:
        m_plain *= m
    m_plain %= n
    try:
        print(bytes.fromhex(hex(m)[2:]))
        print(sum_ed)
    except:
        continue