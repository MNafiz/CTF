from pwn import *
import string

# print(len(string.printable))

# with open("flag.txt", "w") as f:
#     f.write(string.printable)
#     f.close()

mapp = "11 12 10 13 14 39 118 119 123 124 100 85 86 87 91 92 68 56 57 58 59 60 61 40 41 42 43 44 45 46 47 32 33 34 35 36 37 38 93 94 95 77 78 79 80 81 82 83 84 69 70 71 72 73 74 75 76 64 88 89 90 65 66 67 125 126 127 109 110 111 112 113 114 115 116 101 102 103 104 105 106 107 108 96 120 121 122 97 98 99 62 63 48 49 50 51 52 53 54 55".split()[::-1]
hash_map = dict(zip(mapp, list(string.printable)))
# print(hash_map)

context.log_level = "warn"

NC = "nc 103.152.242.228 2021".split()

r = remote(NC[1], NC[2])

r.sendlineafter(b"name: ", b"a")
r.recvuntil(b"flag:")
r.recvline()
result = r.recvline(0).decode().split()[::-1]
result = "".join(hash_map[i] for i in result)
print(result)

r.close()