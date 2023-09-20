from pwn import *
import json
from pkcs1 import emsa_pkcs1_v15
from Crypto.Util.number import *
import re
import secrets

r = remote("socket.cryptohack.org", 13394)
BIT_LENGTH = 768

MSG = b'We are hyperreality and Jack and we own CryptoHack.org'
DIGEST = emsa_pkcs1_v15.encode(MSG, BIT_LENGTH // 8)
BTC_PAT = re.compile("^Please send all my money to ([1-9A-HJ-NP-Za-km-z]+)$")
print(r.recvline())
send = {'option': 'get_signature'}
send = json.dumps(send).encode()
r.sendline(send)

data = json.loads(r.recvline().decode())
N = int(data["N"], 16)
E = int(data["E"], 16)
signature = int(data["signature"], 16)
print(N)
print(E)


def btc_check(msg):
    alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    addr = BTC_PAT.match(msg)
    if not addr:
        return False
    addr = addr.group(1)
    raw = b"\0" * (len(addr) - len(addr.lstrip(alpha[0])))
    res = 0
    for c in addr:
        res *= 58
        res += alpha.index(c)
    raw += long_to_bytes(res)

    if len(raw) != 25:
        return False
    if raw[0] not in [0, 5]:
        return False
    return raw[-4:] == hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4]


alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
raw = b"\x00" * 21
last = hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4]
res = bytes_to_long(last)
ad = ""
while res > 0:
    ad = alpha[res % 58] + ad
    res //= 58
msg = "Please send all my money to " + ("1" * 21) + ad

send = {'option': 'set_pubkey', 'pubkey': hex(22112521820758463818486771827146604356684841190422446613129536516125368128269298120759108640342725723259844097042530947134462898483758214154459142068973563534885822463420677810170927696198579267843561687338126897299431333991771201)}
print(send)

suffix = "fc5aac8e4783dcd760dab9346ce22f2eec20ef95f2e3ace769070ec736619cb5"
msg += suffix
print("msg =", bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), BIT_LENGTH // 8)))
print("signature =", signature)

n = 22112521820758463818486771827146604356684841190422446613129536516125368128269298120759108640342725723259844097042530947134462898483758214154459142068973563534885822463420677810170927696198579267843561687338126897299431333991771201
e = 2735472421614528508549532576358082616117739038258519444581675385993598587506991506953907851618539042409099301976342148270408438477868619729968042916202257533594916613944141519162029294704710381374903481522743185761186994032043710
print(pow(signature, e, n) - bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), BIT_LENGTH // 8)))
print(hex(e))
print(msg)
print(hex(2))
flag = bytes.fromhex("c564cf7bac72221435662823988c49e7dc0e73309e11fdf17accca1a4fed0afca4561c451106d54629cdb14c")

PATTERNS = [
    re.compile(r"^This is a test(.*)for a fake signature.$").match,
    re.compile(r"^My name is ([a-zA-Z\s]+) and I own CryptoHack.org$").match,
    btc_check
]

m0 = "This is a test.for a fake signature."
print(PATTERNS[0](m0))
m0 += suffix
print("msg =", bytes_to_long(emsa_pkcs1_v15.encode(m0.encode(), BIT_LENGTH // 8)))
e = 4508457011298133967459221294492084542865642219333513974291488548822293939298603167119010677759003845879117001788467226558814425466685310162825973669478123875363018051585177658655998412040272110660844469409926164413718314810341439
print(pow(signature, e, n) - bytes_to_long(emsa_pkcs1_v15.encode(m0.encode(), BIT_LENGTH // 8)))
print(hex(e))
print(m0)
f0 = bytes.fromhex("75f02562d36d9e4bb8643095463329b4067217f5bedf4d87ba7f8ad473987b59db0ac40300a88da01e8d006d")

m1 = "My name is Nhat and I own CryptoHack.org"
print(PATTERNS[1](m1))
m1 += suffix
print("msg =", bytes_to_long(emsa_pkcs1_v15.encode(m1.encode(), BIT_LENGTH // 8)))
e = 1467807901683002799264431072576118235342301323754486688404805515629151705152059890116716695908855792559105484144690066746261622687721342966454892735436358599194021707097230941197844823053272584073262504937924133155074676999502687
print(pow(signature, e, n) - bytes_to_long(emsa_pkcs1_v15.encode(m1.encode(), BIT_LENGTH // 8)))
print(hex(e))
print(m1)
f1 = bytes.fromhex("d3e693690b70c733e8763fc581db0530a80514b17fb984059fc770a163100bfa1b33877765f139810371df5c")
print(xor(flag, xor(f1, f0)))