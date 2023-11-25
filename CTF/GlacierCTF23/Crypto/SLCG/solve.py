from Crypto.Util.number import *
from functools import reduce
from output import *

# FLAG = b"gctf{???????}"

class LCG:
    def __init__(self, mod: int, mult: int, add: int, seed: int):
        self.mod = mod
        self.mult = mult
        self.add = add
        self.value = seed

    def __next__(self) -> int:
        self.value = (self.value * self.mult + self.add) % self.mod
        return self.value

    def __iter__(self):
        return self

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
    return multiplier


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(GCD, zeroes))
    return modulus

print(len(ct) // 7 )

ct = [ct[i:i+7] for i in range(0, len(ct), 7)]
bit = list(map(int, list(bin(ord("g"))[2:].zfill(7))))
tes = ct[0]

state_1 = [tes[i] for i in range(len(tes)) if bit[i]]
# print(state_1)

modulus = crack_unknown_modulus(state_1)
multiplier = crack_unknown_multiplier(state_1, modulus)
increment = crack_unknown_increment(state_1, modulus, multiplier)

print(modulus, multiplier, increment)

lcgs = LCG(modulus, multiplier, increment, state_1[0])
for i in range(4):
    next(lcgs)
# lcgs = LCG(next(lcgs), next(lcgs), next(lcgs), next(lcgs))
# print(next(lcgs))
# print(bin(ord("c")))
# print(ct[1])

temp = next(lcgs)
plain_tot = ""


for hh in ct[1:]:
    plain = ""
    lcgs = LCG(temp, next(lcgs), next(lcgs), next(lcgs))
    temp = next(lcgs)
    for h in hh:
        if h == temp:
            plain += "1"
            temp = next(lcgs)
        else:
            plain += "0"
    plain_tot += plain.zfill(8)


flag = b"g" + long_to_bytes(int(plain_tot,2))
print(flag)