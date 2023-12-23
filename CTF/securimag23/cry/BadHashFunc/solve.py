
from pwn import *

payload = ""
a = "7563667261747d00"
a = bytes.fromhex(a)

for i in range(len(a)):
    payload += hex((a[i] & 0xf0) >> 4)[2:] + "11" + hex(a[i] & 0x0f)[2:]

def pack(message):
    """
    Pack the message to an integer

    :param message bytes: message to hash
    """
    ret = 0
    if len(message) % 2:
        message += b'\x00'
    for ind in range(0,len(message),2):
        ret |= (message[ind] & 0xf0)
        ret |= (message[ind+1] & 0x0f)
        ret <<= 8
    return ret

def hash(message):
    """
    Make the hash of a given string

    :param message string: message to hash
    """
    packed_message = pack(message.encode())
    hash = packed_message % 2**64
    hash_str = hex(hash)[2:]
    return hash_str

print(payload, len(payload))
print(hash(payload))

nc = "nc ctf.securimag.org 1058".split()

r = remote(nc[1], nc[2])

r.sendline(bytes.fromhex(payload))


r.interactive()