flag = open("flag.txt", "rb").read() 
key = open("/dev/urandom", "rb").read(30) # Longer plaintext, longer key, you wont break this one !

encrypted = []
for i,c in enumerate(flag):
    encrypted += [c ^ key[i % len(key)]]

with open("output.bin", "wb") as fd:
    fd.write(bytes(encrypted))



