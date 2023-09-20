import base64

import jwt
import requests
import json


def get_pubkey():
    r = requests.get("https://web.cryptohack.org/rsa-or-hmac/get_pubkey/")
    return json.loads(r.text)["pubkey"]


def create_session(username):
    r = requests.get(f"https://web.cryptohack.org/rsa-or-hmac/create_session/{username}/")
    return r.text


def authorise(token):
    r = requests.get(f"https://web.cryptohack.org/rsa-or-hmac/authorise/{token}/")
    return r.text


def login():
    pub_key = get_pubkey()
    token = jwt.encode({'username': 'nhat', 'admin': 'true'}, pub_key, 'HS256')
    return token


token = login()
print(authorise(token))