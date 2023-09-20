from sage.all import *

exec(open("output.txt").read())

scale_value = 2**65

mat = Matrix(ZZ,[
    [scale_value,e],
    [0,-n]
])

mat = mat.LLL()

d = mat[0][0] // scale_value

m = pow(c,d,n)

print(bytes.fromhex(hex(m)[2:]))