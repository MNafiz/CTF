import sys

with open(sys.argv[1], "rb") as f:
    encryptedData = f.read()
    f.close()

def decryptCaesar(encrypted):
    messageByte = []
    for i in range(len(encrypted)):
        tmp = encrypted[i]
        if((tmp >= 65) and (tmp <= 90)):
            res = (tmp - 65 + 13) % 26 + 65
        elif((tmp >= 97) and (tmp <= 122)):
            res = (tmp - 97 + 13) % 26 + 97
        else:
            res = tmp
        messageByte.append(res)
    message = bytes(messageByte)
    return message

print(decryptCaesar(encryptedData).decode())

"""
$ python3 recover.py File_Berharga.txt.hack
b'secret_key = "jago bisa balikin file ini"
"""
