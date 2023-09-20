from Crypto.Util.number import bytes_to_long
from base64 import urlsafe_b64decode

b64p = lambda x : x + b"=" * (4 - len(x) % 4)

token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiY3J5cHRve2p3dF9jb250ZW50c19jYW5fYmVfZWFzaWx5X3ZpZXdlZH0iLCJ1c2VyIjoiQ3J5cHRvIE1jSGFjayIsImV4cCI6MjAwNTAzMzQ5M30.shKSmZfgGVvd2OSB2CGezzJ3N6WAULo3w9zCl_T47KQ"


header, payload, signature = [urlsafe_b64decode(b64p(i)) for i in token.split(b".")]


print(header)
print(payload)
print(bytes_to_long(signature))