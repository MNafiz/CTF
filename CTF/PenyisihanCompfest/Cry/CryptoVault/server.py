#!/bin/env python3
import ecdsa
import ecdsa.ellipticcurve as EC
import binascii
import ecdsa.util
import json

curve = ecdsa.SECP256k1
G = curve.generator
n = G.order()
x = int('ce205d44c14517ba33f3ef313e404537854d494e28fcf71615e5f51c9a459f42', 16)
y = int('6080e22d9a44a5ce38741f8994ac3a14a6760f06dd1510b89b6907dfd5932868', 16)
Q = EC.Point(curve.curve, x, y)
PUBKEY = ecdsa.VerifyingKey.from_public_point(Q, curve)

# Convert the public key to standard format
PUBKEY_str = binascii.hexlify(PUBKEY.to_string()).decode()

def verify_signature(data):
    signature_hex = data['signature']
    message_hash = int(data['message_hash'], 16)
    # print(message_hash)
        # Convert the signature from standard format
    signature_bin = binascii.unhexlify(signature_hex)
    r = int.from_bytes(signature_bin[:32], 'big')
    s = int.from_bytes(signature_bin[32:], 'big')
    sig = ecdsa.ecdsa.Signature(r, s)
    
    result = verify_ecdsa_signature(sig, message_hash)
    
    response = {'result': result, 'pubkey': PUBKEY_str}
    return response

def verify_ecdsa_signature(sig, message_hash):
    m = message_hash
    if PUBKEY.pubkey.verifies(m, sig):
        return "COMPFEST15{bad_implementation_ecdsa}"
    else:
        return "skill issue ( ͡° ͜ʖ ͡°)"

if __name__ == '__main__':
    try:
        data = json.loads(input("Verify your signature here: "))
        response = verify_signature(data)
        print(response["result"])
    except Exception as e:
        print("something wrong happened!")
        print(e)