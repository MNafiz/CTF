from sage.all import *
from pwn import *
from Crypto.Util.number import *
from functools import reduce

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)

class generator():
	def __init__(self,a,c,m,seed):
		self.a=a
		self.c=c
		self.m=m
		self.seed=seed%self.m
		U=[]
		for i in range(64):
			U.append([])
			for j in range(64):
				if j==i+1:
					U[i].append(1)
				else:
					U[i].append(0)
		U=Matrix(GF(2),U)
		L=[]
		for i in range(64):
			L.append([])
			for j in range(64):
				if j==i-1:
					L[i].append(1)
				else:
					L[i].append(0)
		L=Matrix(GF(2),L)
		self.U=U
		self.L=L
		
	def next(self):
		res=self.seed
		res='{:064b}'.format(res)
		res=vector(GF(2),list(res))
		res=res+((self.U**13)*res)
		res=res+((self.L**21)*res)
		res=''.join([str(i) for i in res])
		res=int(res,2)
		self.seed=(self.a*self.seed+self.c)%self.m
		return res


#p = process("./chall.py")

p = remote("103.152.242.197", 54259)

def get_state(x,y,getFlag=False):
    p.sendlineafter(b"$ ", f"{x},{y}".encode())
    if getFlag:
	    p.recvuntil(b"untukmu")
	    print(p.recvline(0))
	    return
    p.recvuntil(b"koordinat ")
    state_enc_1, state_enc_2 = [int(i) for i in p.recvline(0).decode().split(",")]
    return state_enc_1, state_enc_2

def decrypt_state(x,y):
    x = [int(i) for i in bin(x)[2:].zfill(64)]
    y = [int(i) for i in bin(y)[2:].zfill(64)]
    for i in range(21,len(x)):
        x[i] ^^= x[i-21]
        y[i] ^^= y[i-21]
    for j in range(len(x)-14,-1,-1):
        x[j] ^^= x[j+13]
        y[j] ^^= y[j+13]
    x = int("".join([str(i) for i in x]),2)
    y = int("".join([str(i) for i in y]),2)
    return x,y

state = []
for i in range(3):
    enc_1, enc_2 = get_state(1,1)
    state_1, state_2 = decrypt_state(enc_1,enc_2)
    state.extend([state_1,state_2])

modulus, multiplier, increment = crack_unknown_modulus(state)
gen = generator(multiplier,increment,modulus,state[-1])
gen.next()

x = gen.next()
y = gen.next()

get_state(x,y,getFlag=True)

p.close()