from Crypto.Cipher import AES

key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'

cipher =  AES.new(key,AES.MODE_ECB)

print(cipher.decrypt(ciphertext))