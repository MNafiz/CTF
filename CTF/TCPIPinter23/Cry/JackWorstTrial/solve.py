import jwt

from Crypto.PublicKey import RSA


with open('./mykey.pem', 'rb') as f:
   PRIVATE_KEY = f.read()

with open('./pubKey.pem', 'rb') as f:
   PUBLIC_KEY = f.read()

key = RSA.import_key(PRIVATE_KEY)
token = jwt.encode({
				'public_id': "a",
				'name': "b",
				'admin': False,
				'exp' : 10000000000000000000000
			}, PRIVATE_KEY, algorithm='RS256')

print(token)

print(jwt.decode(token, PUBLIC_KEY))



token = jwt.encode({
				'public_id': "a",
				'name': "b",
				'admin': False,
				'exp' : 10000000000000000000000
			}, None, algorithm='none')

print(token)
print(jwt.decode(token, None))