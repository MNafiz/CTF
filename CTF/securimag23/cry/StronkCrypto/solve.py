from pwn import *
import string

pos = string.printable.strip().encode()
ct = "c7dab9a24b5e617d31e353d3c22049cf7a5682afd43ccb8db038a35c7c5241d460dea7c5906a4ba11a936a2faff7753687aeac7652c2f44f3a69f551c564562aa6aef386f9abdf886b46aaed393f1224e5a0b1e6bffd0720a0a94c59fdab767368de7859f885c7e7ae2cdfc7f6ee50e2515e4571f94a07004dd0d1ab63ed7fdf51844483c7059342688f59a705e153fcd893a4c83d1aa8e7abe7d5dd72d51337a18d4068fecfa9c08978b63ef31f74b97a5682afd43ccb8db038a35c7c5241d4b48fe52eabb177a2443b7b6b022f882bb48fe52eabb177a2443b7b6b022f882b23f38e391a20ed56ae14a350860ad301aff9bf37a53e1506b1a295b4e00637414e4a61ce8eac0b1c7d39f85059a5166c6d958148c20c3dcb6af1bad2b24fc39823f38e391a20ed56ae14a350860ad301887817da53f347c6ee256b87cde982d24e4a61ce8eac0b1c7d39f85059a5166c23f38e391a20ed56ae14a350860ad301887817da53f347c6ee256b87cde982d26d958148c20c3dcb6af1bad2b24fc398a6aef386f9abdf886b46aaed393f12244e4a61ce8eac0b1c7d39f85059a5166caff9bf37a53e1506b1a295b4e0063741554671c91deae3885f1396f625e0096a23f38e391a20ed56ae14a350860ad301515e4571f94a07004dd0d1ab63ed7fdfe2426407af12d5a537555dba7c43d03a6d958148c20c3dcb6af1bad2b24fc3987a5682afd43ccb8db038a35c7c5241d4a6aef386f9abdf886b46aaed393f122423f38e391a20ed56ae14a350860ad301515e4571f94a07004dd0d1ab63ed7fdfb48fe52eabb177a2443b7b6b022f882bb48fe52eabb177a2443b7b6b022f882b19b8ed01c5ce538b0e3a7f13f645c760"
ct = bytes.fromhex(ct)
ct = [ct[i:i+16] for i in range(0, len(ct), 16)]



NC = "nc ctf.securimag.org 1061".split()

r = remote(NC[1], NC[2])

r.sendlineafter(b">", pos)
r.recvuntil(b"Okay its ")
result = r.recvline(0).decode()

result = bytes.fromhex(result)
print(len(result) // 16, len(pos))
result = [result[i:i+16] for i in range(0, len(result), 16)]

mapping = dict()
for i, res in zip(pos, result):
    mapping[res] = i

flag = b""
for i in ct:
    flag += bytes([mapping[i]])
    # print(flag)

print(flag)

r.interactive()