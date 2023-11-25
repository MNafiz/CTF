from pwn import *
from Crypto.Util.Padding import *
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

NC = "nc 103.145.226.206 1945".split()

NC = "nc 103.145.226.209 1945".split()

r = remote(NC[1], NC[2])

def goto(n):
    r.sendlineafter(b">> ", str(n).encode())

def tes(msg):
    goto(1)
    r.sendlineafter(b"pesan: ", msg.hex().encode())
    r.recvuntil(b"Ciphertext = ")
    result = bytes.fromhex(r.recvline(0).decode())
    return result

r.recvuntil(b"enckey = ")
enckey = bytes.fromhex(r.recvline(0).decode())

r.recvuntil(b"enccode = ")
enccode = eval(r.recvline(0))

r.recvuntil(b"iv2 = ")
iv2 = eval(r.recvline(0))


print(tes(b"a"))
print(enckey)


print(len(enckey))

key = b""
for i in range(len(enckey)):
    print(i+1)
    for j in range(256):
        hasil = key + bytes([j])
        hasilenc = tes(hasil)
        if hasilenc == enckey[:len(hasilenc)]:
            key += bytes([j])
            print(key)
            break


assert tes(key) == enckey

key = key[:16]

for i in range(65536):
    print(i)
    posKey = key + long_to_bytes(i)*8
    cipher = AES.new(posKey,AES.MODE_CBC, iv2)
    hasil = cipher.decrypt(enccode)
    if b"Very" in hasil:
        print(unpad(hasil, 16))
        break

goto(2)
r.sendline(unpad(hasil, 16))

r.interactive()

# NCW23{kenapa_bocor_lagi_yak_keynya?_yang_penting_soalnya_simple_dah}
# 2d2d2d2d2d424547494e20444820504152414d45544552532d2d2d2d2d0a4d455943515144576d6f446354796c414c50575a68496c6a3573747359783872644a4b626d6e4e7772393031637a42726669564b7933616c6d323175794473460a7331302f72467848514a68626358527773532b7835712f5363584c76416745430a2d2d2d2d2d454e4420444820504152414d45544552532d2d2d2d2d