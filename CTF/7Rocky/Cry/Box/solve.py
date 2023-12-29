from Crypto.Util.number import *

ct = 5545457088879574964209613711409478327714366805681091501255101702161458272094830554232779120250  
box_1337 = 3011454617406654839679120250
box_0x1337 = 10002638090931457241529120250

a = (box_0x1337 - box_1337) // (0x1337 - 1337)
b = box_1337 - a*1337

m = (ct - b) // a
flag = long_to_bytes(m).decode()

print(flag)