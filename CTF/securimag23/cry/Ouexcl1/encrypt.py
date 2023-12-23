
flag = b"redacted, t'as cru quoi??"

key = open("/dev/urandom", "rb").read(10)

encrypted = []
for i,c in enumerate(flag):
    encrypted += [c ^ key[i % len(key)]]

with open("output.bin", "wb") as fd:
    fd.write(bytes(encrypted))



