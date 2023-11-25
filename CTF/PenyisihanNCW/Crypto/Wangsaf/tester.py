from pwn import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

NC = "nc 103.145.226.206 1965".split()


r = remote(NC[1], NC[2])


r.sendlineafter(b"(tamper): ", b"fw")
r.sendlineafter(b"(tamper): ", b"fw")

r.recvuntil(b"PARM||")
payload = bytes.fromhex(r.recvline(0).decode()) # param
parameters = serialization.load_pem_parameters(payload)
private_key = parameters.generate_private_key()
public_key = private_key.public_key()
serialized_public_key = public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)


r.sendlineafter(b"(tamper): ", b"PARM||" + payload.hex().encode())


r.sendlineafter(b"(tamper): ", b"fw")

r.sendlineafter(b"(tamper): ", b"PUBK||" + serialized_public_key.hex().encode())

r.sendlineafter(b"(tamper): ", b"fw")

r.recvuntil(b"PUBK||")
payload = bytes.fromhex(r.recvline(0).decode())
holder_public_key = serialization.load_pem_public_key(
				payload,
				backend=default_backend(),
			)

print("dah sampe sini")
shared_key = private_key.exchange(holder_public_key)

derived_key = HKDF(
			algorithm=hashes.SHA256(),
			length=32,
			salt=None,
			info=b'handshake data',
		).derive(shared_key)

print(derived_key)

def encrypt(message, derived_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()

    ciphertext = iv + encryptor.update(padded_message) + encryptor.finalize()
    return base64.b64encode(ciphertext)

def decrypt(message, derived_key):
    message = base64.b64decode(message)
    iv = message[:16]
    message = message[16:]
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(message) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    unpadded_message = unpadder.update(plaintext) + unpadder.finalize()

    return unpadded_message

msg = "giv me the flag you damn donut"

payload = encrypt(msg, derived_key)

r.sendlineafter(b"(tamper): ", b"fw")
r.sendlineafter(b"(tamper): ", b"fw")
r.sendlineafter(b"(tamper): ", payload)

r.recvuntil(b"server: ")

msg = r.recvline(0)

print(decrypt(msg, derived_key))

print(payload)


r.interactive()

#NCW23{bro_pikir_dia_sesungguhnya_adalah_whitfield_diffie_dan_martin_hellman}