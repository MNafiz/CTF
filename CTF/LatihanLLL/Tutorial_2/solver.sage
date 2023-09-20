from sage.all import *

# S = 35198493525058225869121455658069026374446
# public = [38570022767253596282892436519217876464, 66565567473661431158058192094705415619, 171137441585705537841798357794749950853]

with open("output.txt","r") as f:
    exec(f.read())
    f.close()

M = Matrix([
    [1,0,0,public[0]],
    [0,1,0,public[1]],
    [0,0,1,public[2]],
    [0,0,0,-S]
])

res = M.LLL()

S_val = sum([public[i]*res[0][i] for i in range(3)])

if S_val == S:
    print("LLL works!")