import requests
import json
from Crypto.Cipher import ARC4
import string
from Crypto.Util.number import long_to_bytes, bytes_to_long


def send_cmd(ciphertext, nonce):
    r = requests.get(f"https://aes.cryptohack.org/oh_snap/send_cmd/{ciphertext}/{nonce}/")
    return json.loads(r.text)["error"].split("Unknown command: ")[1]


ciphertext = b"\x00"
size = 256 - 222
print(size)
alphabet = string.ascii_letters + string.digits + "_" + "@" + "!" + "$" + "{" + "}" + "?"
flag = "crypto{w1R3d_equ1v4l3nt_pr1v4cy?!}"

n = 3 + len(flag)
while len(flag) < 50:
    lib = {}
    s = n * (n + 1) // 2
    for c in flag:
        s += ord(c)
    for v in range(256):
        nonce = bytes([n]) + bytes([255]) + bytes([v])
        cmd = send_cmd(ciphertext.hex(), nonce.hex())
        cmd = int(cmd, 16)
        c = chr((cmd - v - s) % 256)
        if not (c in alphabet):
            continue
        if c in lib:
            lib[c] += 1
        else:
            lib[c] = 1
    print("-------")
    print(lib)
    m = 0
    f = '.'
    for c in lib:
        if lib[c] > m:
            f = c
            m = lib[c]
    flag += f
    print(flag)
    print("length =", len(flag))
    n += 1