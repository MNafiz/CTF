from Crypto.PublicKey import RSA

with open("key.pub", "r") as f:
    key = RSA.import_key(f.read())
    f.close()

print(key.n)