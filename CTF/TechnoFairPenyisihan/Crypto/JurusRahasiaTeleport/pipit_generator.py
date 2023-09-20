from random import getrandbits
from Crypto.Util.number import *
from sage.all import *
class generator():
	def __init__(self):
		self.a=getrandbits(64)
		self.c=getrandbits(64)
		self.m=getPrime(64)
		self.seed=getrandbits(64)%self.m
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