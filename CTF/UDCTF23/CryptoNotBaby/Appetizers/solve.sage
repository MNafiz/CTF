from sage.all import *

choices = [19728964, 30673077, 137289540, 195938621, 207242611, 237735979, 298141799, 302597011, 387047012, 405520686, 424852916, 461998372, 463977415, 528505766, 557896298, 603269308, 613528675, 621228168, 654758801, 670668388, 741571487, 753993381, 763314787, 770263388, 806543382, 864409584, 875042623, 875651556, 918697500, 946831967]
target = 7627676296

matrix = Matrix(ZZ, 31, 31)

N = int(sqrt(len(choices))) // 2

for i in range(30):
    matrix[i, -1] = choices[i] * N
    matrix[i, i] = 2
    matrix[-1, i] = -1
matrix[-1, -1] = -target * N

res = matrix.LLL()
for row in res:
    if row[-1] == 0:
        print(row)