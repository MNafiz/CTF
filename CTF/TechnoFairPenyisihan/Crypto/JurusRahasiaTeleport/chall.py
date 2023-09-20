#!/usr/bin/python3

from pipit_generator import generator

flag = "TechnoFairCTF2023{congrats_ini_flagnya!}"

gen=generator()
chance=4
while chance>0:
	chance-=1
	print(f"tebak angka pipit selanjutnya !")
	inp_user=input(f"$ ")
	x_pred,y_pred=inp_user.split(',')
	x_pred,y_pred=int(x_pred),int(y_pred)
	x,y=gen.next(),gen.next()
	if(x_pred==x and y_pred==y):
		print(f"Pipit berhasil ditangkap! ini untukmu! {flag}")
	else:
		print(f"lokasi yang kamu berikan salah!")
		print(f"Pipit ditemukan pada posisi koordinat {x},{y}")
