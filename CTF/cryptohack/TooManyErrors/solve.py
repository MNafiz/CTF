from pwn import *
import json

NC = "nc socket.cryptohack.org 13390".split()

r = remote(NC[1], NC[2])

def get_sample():
    payload = dict()
    payload["option"] = "get_sample"
    r.sendline(json.dumps(payload).encode())
    result = json.loads(r.recvline(0))
    return result

def reset():
    payload = dict()
    payload["option"] = "reset"
    r.sendline(json.dumps(payload).encode())
    r.recvline(0)

def different(a , b):
    result = [ai != bi for ai, bi in zip(a, b)]
    try:
        idx = result.index(True)
    except:
        idx = False
    return sum(result) , idx

q = 127
r.recvuntil(b"option.\n")

flag = [0x20 for _ in range(28)]
idxs = []

while (0x20 in flag):
    sampleOne = get_sample()
    reset()
    sampleTwo = get_sample()
    reset()
    # print(sampleOne)
    # print(sampleTwo)
    dif, idx = different(sampleOne["a"], sampleTwo["a"])
    print(dif)
    if (dif == 1) and (idx not in idxs):
        flagChar = ((sampleTwo["b"] - sampleOne["b"]) * pow(sampleTwo["a"][idx] - sampleOne["a"][idx], -1 , q)) % q
        flag[idx] = flagChar
        idxs.append(idx)
        print(bytes(flag))
    print("="*10)

r.interactive()
