from hashlib import sha1
from Crypto.Util.number import *
from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key
from random import randint

G = generator_256
q = G.order()

FLAG = b'crypto{??????????????????}'

sig1 = {'msg': 'I have hidden the secret flag as a point of an elliptic curve using my private key.', 'r': '0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae', 's': '0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d'}
sig2 = {'msg': 'The discrete logarithm problem is very hard to solve, so it will remain a secret forever.', 'r': '0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c', 's': '0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8'}
sig3 = {'msg': 'Good luck!', 'r': '0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6', 's': '0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba'}
h1 = sha1(sig1['msg'].encode()).digest()
h2 = sha1(sig2['msg'].encode()).digest()
h3 = sha1(sig3['msg'].encode()).digest()
hidden_flag = (16807196250009982482930925323199249441776811719221084165690521045921016398804, 72892323560996016030675756815328265928288098939353836408589138718802282948311)
pubkey = (48780765048182146279105449292746800142985733726316629478905429239240156048277, 74172919609718191102228451394074168154654001177799772446328904575002795731796)
p = curve_256.p()
G_d = ellipticcurve.Point(curve_256, pubkey[0], pubkey[1])
T = ellipticcurve.Point(curve_256, hidden_flag[0], hidden_flag[1])
S1 = inverse(int(sig1['s'], 16), q) * (bytes_to_long(h1) * G + int(sig1['r'], 16) * G_d)
S2 = inverse(int(sig2['s'], 16), q) * (bytes_to_long(h2) * G + int(sig2['r'], 16) * G_d)
S3 = inverse(int(sig3['s'], 16), q) * (bytes_to_long(h3) * G + int(sig3['r'], 16) * G_d)
r1 = int(sig1['r'], 16)
s1 = int(sig1['r'], 16)
r2 = int(sig2['r'], 16)
s2 = int(sig2['r'], 16)
r3 = int(sig3['r'], 16)
s3 = int(sig3['r'], 16)

B = bytes_to_long(b"\xff" * 20)
print(B)
print(q)

d = 110104254168941847244659959021870001852301044662581657616531508669991620749093
d_inv = inverse(d, q)
Q = d_inv * T
print(long_to_bytes(Q.x()))