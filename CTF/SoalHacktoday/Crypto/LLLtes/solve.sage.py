

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_100 = Integer(100); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_4 = Integer(4); _sage_const_0 = Integer(0)
from sage.all import *
from Crypto.Util.number import *
from gmpy2 import *
from itertools import product

with open("output.txt","r") as f:
    exec(f.read())
    f.close()

batas = _sage_const_100 
number_list = list(range(_sage_const_1 ,batas+_sage_const_1 ))

list_product = [i*j for i, j in list(product(number_list,repeat=_sage_const_2 ))]
list_product = list(set(list_product))

hint_1_quad = hint_1**_sage_const_2 
for prod in list_product:
    temp = iroot(hint_1_quad + _sage_const_4  * prod * n, _sage_const_2 )
    if temp[_sage_const_1 ]:
        print(prod)
        hint_2 = int(temp[_sage_const_0 ])

