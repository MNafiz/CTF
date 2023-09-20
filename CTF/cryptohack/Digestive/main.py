import json
from ecdsa.keys import SigningKey, _truncate_and_convert_digest
from ecdsa._compat import normalise_bytes
import requests

SK = SigningKey.generate()  # uses NIST192p
VK = SK.verifying_key


def sign(username):
    r = requests.get(f"https://web.cryptohack.org/digestive/sign/{username}/")
    return json.loads(r.text)


def verify(msg, signature):
    r = requests.get(f"https://web.cryptohack.org/digestive/verify/{msg}/{signature}/")
    return r.text


username = "admin"
data = sign(username)
print(data)
msg = data["msg"]
signature = data["signature"]
digest = normalise_bytes(msg.encode())
print(_truncate_and_convert_digest(digest, SK.curve, True))
msg = "{\"admin\": false, \"username\": \"admin\", \"admin\": true}"
digest = normalise_bytes(msg.encode())
print(_truncate_and_convert_digest(digest, SK.curve, True))
print(verify(msg, signature))