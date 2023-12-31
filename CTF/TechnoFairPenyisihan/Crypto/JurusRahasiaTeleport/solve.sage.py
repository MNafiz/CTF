

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_64 = Integer(64); _sage_const_13 = Integer(13); _sage_const_21 = Integer(21); _sage_const_54259 = Integer(54259); _sage_const_14 = Integer(14); _sage_const_3 = Integer(3)
from sage.all import *
from pwn import *
from Crypto.Util.number import *
from functools import reduce

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[_sage_const_1 ] - states[_sage_const_0 ]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[_sage_const_2 ] - states[_sage_const_1 ]) * inverse(states[_sage_const_1 ] - states[_sage_const_0 ], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[_sage_const_1 :])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[_sage_const_1 :], diffs[_sage_const_2 :])]
    modulus = abs(reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)

class generator():
	def __init__(self,a,c,m,seed):
		self.a=a
		self.c=c
		self.m=m
		self.seed=seed%self.m
		U=[]
		for i in range(_sage_const_64 ):
			U.append([])
			for j in range(_sage_const_64 ):
				if j==i+_sage_const_1 :
					U[i].append(_sage_const_1 )
				else:
					U[i].append(_sage_const_0 )
		U=Matrix(GF(_sage_const_2 ),U)
		L=[]
		for i in range(_sage_const_64 ):
			L.append([])
			for j in range(_sage_const_64 ):
				if j==i-_sage_const_1 :
					L[i].append(_sage_const_1 )
				else:
					L[i].append(_sage_const_0 )
		L=Matrix(GF(_sage_const_2 ),L)
		self.U=U
		self.L=L
		
	def next(self):
		res=self.seed
		res='{:064b}'.format(res)
		res=vector(GF(_sage_const_2 ),list(res))
		res=res+((self.U**_sage_const_13 )*res)
		res=res+((self.L**_sage_const_21 )*res)
		res=''.join([str(i) for i in res])
		res=int(res,_sage_const_2 )
		self.seed=(self.a*self.seed+self.c)%self.m
		return res


#p = process("./chall.py")

p = remote("103.152.242.197", "54259" )

def get_state(x,y,getFlag=False):
    p.sendlineafter(b"$ ", f"{x},{y}".encode())
    if getFlag:
	    p.recvuntil(b"untukmu! ")
	    print(p.recvline(_sage_const_0 ))
	    return
    p.recvuntil(b"koordinat ")
    state_enc_1, state_enc_2 = [int(i) for i in p.recvline(_sage_const_0 ).decode().split(",")]
    return state_enc_1, state_enc_2

def decrypt_state(x,y):
    x = [int(i) for i in bin(x)[_sage_const_2 :].zfill(_sage_const_64 )]
    y = [int(i) for i in bin(y)[_sage_const_2 :].zfill(_sage_const_64 )]
    for i in range(_sage_const_21 ,len(x)):
        x[i] ^= x[i-_sage_const_21 ]
        y[i] ^= y[i-_sage_const_21 ]
    for j in range(len(x)-_sage_const_14 ,-_sage_const_1 ,-_sage_const_1 ):
        x[j] ^= x[j+_sage_const_13 ]
        y[j] ^= y[j+_sage_const_13 ]
    x = int("".join([str(i) for i in x]),_sage_const_2 )
    y = int("".join([str(i) for i in y]),_sage_const_2 )
    return x,y

state = []
for i in range(_sage_const_3 ):
    enc_1, enc_2 = get_state(_sage_const_1 ,_sage_const_1 )
    state_1, state_2 = decrypt_state(enc_1,enc_2)
    state.extend([state_1,state_2])

modulus, multiplier, increment = crack_unknown_modulus(state)
gen = generator(multiplier,increment,modulus,state[-_sage_const_1 ])
gen.next()

x = gen.next()
y = gen.next()

get_state(x,y,getFlag=True)

p.close()

