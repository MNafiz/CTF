from Crypto.Util.number import bytes_to_long

flag = open("flag.txt", "rb").read().strip()

TABLE = [
    lambda a, b: f"({a}+{b})",
    lambda a, b: f"({a}-{b})",
    lambda a, b: f"({a}*{b})",
]


def build_box(s: bytes):
    e = "(x)"
    for b in s:
        e = TABLE[b % len(TABLE)](e, b)
    return eval(f"lambda x: {e}")


box = build_box(flag)
ct = box(bytes_to_long(flag))
print(ct)
print(box(1337))
print(box(0x1337))