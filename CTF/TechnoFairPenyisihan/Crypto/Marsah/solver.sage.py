

# This file was *autogenerated* from the file solver.sage
from sage.all_cmdline import *   # import sage library

_sage_const_6270022 = Integer(6270022); _sage_const_2279888 = Integer(2279888); _sage_const_4611000 = Integer(4611000); _sage_const_6865110 = Integer(6865110); _sage_const_7131265 = Integer(7131265); _sage_const_2632260 = Integer(2632260); _sage_const_6513518 = Integer(6513518); _sage_const_2104512 = Integer(2104512); _sage_const_4979880 = Integer(4979880); _sage_const_6603582 = Integer(6603582); _sage_const_7069254 = Integer(7069254); _sage_const_2909340 = Integer(2909340); _sage_const_7000510 = Integer(7000510); _sage_const_4165180 = Integer(4165180); _sage_const_5579310 = Integer(5579310); _sage_const_3399864 = Integer(3399864); _sage_const_6821210 = Integer(6821210); _sage_const_1579356 = Integer(1579356); _sage_const_5783030 = Integer(5783030); _sage_const_2323732 = Integer(2323732); _sage_const_5394870 = Integer(5394870); _sage_const_4903650 = Integer(4903650); _sage_const_3224572 = Integer(3224572); _sage_const_5965652 = Integer(5965652); _sage_const_4428244 = Integer(4428244); _sage_const_5256540 = Integer(5256540); _sage_const_6759199 = Integer(6759199); _sage_const_1440816 = Integer(1440816); _sage_const_6452644 = Integer(6452644); _sage_const_3200612 = Integer(3200612); _sage_const_5072100 = Integer(5072100); _sage_const_1357692 = Integer(1357692); _sage_const_65382 = Integer(65382); _sage_const_62011 = Integer(62011); _sage_const_60874 = Integer(60874); _sage_const_46110 = Integer(46110); _sage_const_43844 = Integer(43844); _sage_const_27708 = Integer(27708); _sage_const_0 = Integer(0)
from sage.all import *

enc =  [(_sage_const_6270022 , _sage_const_2279888 , _sage_const_4611000 , _sage_const_6865110 , _sage_const_7131265 , _sage_const_2632260 ), (_sage_const_6513518 , _sage_const_2104512 , _sage_const_4979880 , _sage_const_6603582 , _sage_const_7069254 , _sage_const_2909340 ), (_sage_const_7000510 , _sage_const_4165180 , _sage_const_5579310 , _sage_const_3399864 , _sage_const_6821210 , _sage_const_1579356 ), (_sage_const_5783030 , _sage_const_2323732 , _sage_const_5394870 , _sage_const_4903650 , _sage_const_3224572 , _sage_const_2632260 ), (_sage_const_5965652 , _sage_const_4428244 , _sage_const_5256540 , _sage_const_6865110 , _sage_const_6759199 , _sage_const_1440816 ), (_sage_const_6452644 , _sage_const_3200612 , _sage_const_5072100 , _sage_const_3399864 , _sage_const_7131265 , _sage_const_1357692 )]
enc = Matrix(enc)

list_key = [_sage_const_65382 ,_sage_const_62011 ,_sage_const_60874 ,_sage_const_46110 ,_sage_const_43844 ,_sage_const_27708 ]

key = [
    [_sage_const_60874 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ],
    [_sage_const_0 ,_sage_const_43844 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ],
    [_sage_const_0 ,_sage_const_0 ,_sage_const_46110 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ],
    [_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_65382 ,_sage_const_0 ,_sage_const_0 ],
    [_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_62011 ,_sage_const_0 ],
    [_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_0 ,_sage_const_27708 ]
]
key = Matrix(key)

Hasil = enc*key.inverse()

flag = b""
for vec in Hasil:
    flag += bytes(vec)
print(b"TechnoFairCTF{"+flag+b"}")

