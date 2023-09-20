# import ecdsa
# from pycoin.ecdsa import generator_secp256k1, sign, verify

# import hashlib

# def sha3_256Hash(msg):
#     hashBytes = hashlib.sha256(msg.encode("utf8")).digest()
#     return int.from_bytes(hashBytes, byteorder="big")

# def signECDSAsecp256k1(msg, privKey):
#     msgHash = sha3_256Hash(msg)
#     signature = sign(generator_secp256k1, privKey, msgHash)
#     return signature

# def verifyECDSAsecp256k1(msg, signature, pubKey):
#     msgHash = sha3_256Hash(msg)
#     valid = verify(generator_secp256k1, pubKey, msgHash, signature)
#     return valid

curve = ecdsa.SECP256k1
G = curve.generator
n = G.order()
pubKey = 0xce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f426080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868

# # ECDSA sign message (using the curve secp256k1 + SHA3-256)
# msg = "Message for ECDSA signing"
# privKey = secrets.randbelow(generator_secp256k1.order())
# signature = signECDSAsecp256k1(msg, privKey)
# print("Message:", msg)
# print("Private key:", hex(privKey))
# print("Signature: r=" + hex(signature[0]) + ", s=" + hex(signature[1]))


from ecdsa import SigningKey
private_key = SigningKey.generate() # uses NIST192p
signature = private_key.sign(b"Educative authorizes this shot")
print(signature)
public_key = private_key.verifying_key
print("Verified:", public_key.verify(signature, b"Educative authorizes this shot"))