from sage.all import *


exec(open("output.txt").read())

n ,e = pub[1], pub[0]

scale = 2**128

mat = Matrix([
    [scale,e],
    [0,-n]
])

res = mat.LLL()
d = res[0][0] // scale
m = pow(c,d,n)
flag = bytes.fromhex(hex(m)[2:])
print(flag)