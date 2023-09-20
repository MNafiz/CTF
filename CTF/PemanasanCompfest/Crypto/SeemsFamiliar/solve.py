from pwn import *

NC = "nc 34.101.174.85 10000".split()

r = remote(NC[1],NC[2])

def encrypt(message):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"= ", message.hex().encode())
    r.recvuntil(b": ")
    cipher = bytes.fromhex(r.recvline(0).decode())
    return cipher

# for i in range(1,16):
#     result = encrypt(b"a"*i)
#     print(len(result),i)

payload = b"a"*191
payload = list(payload)
flag = ""
for k in range(76):
    print(k+1)
    for i in range(32,127):
        payload[95] = i
        payload_kirim = bytes(payload)
        result = encrypt(payload_kirim)
        if result[80:96] == result[176:192]:
            payload = payload[1:]
            flag += chr(i)
            break
    if len(flag) % 16 == 0:
        print(flag)
    if len(flag) == 76:
        break

print(flag) #COMPFEST15{afdd2f3f203a7ee5055bbadb15302b9c1b81b78a747901fd3232dbd9ff479495}

r.interactive()