# print(open("output2.txt").read())

a = open("important_file.hackedlol","rb").read()
b = open("output4.txt","rb").read()
c = open("hasil","w")

for i in range(len(a)):
    c.write(chr(a[i] ^ b[(i * 0x27) % len(b)]))