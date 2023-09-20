from pwn import *
import json
from Crypto.Util.number import inverse

VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
SUITS = ['Clubs', 'Hearts', 'Diamonds', 'Spades']

deck = [(value, suit) for suit in SUITS for value in VALUES]
print(deck)


def rebase(n, b=52):
    if n < b:
        return [n]
    else:
        return [n % b] + rebase(n // b, b)


r = remote("socket.cryptohack.org", 13383)

arr = []
mod = 2**61 - 1

hand = -1
for _ in range(33):
    if _ > 0:
        send = {'choice': 'h'}
        send = json.dumps(send).encode()
        r.sendline(send)
    data = json.loads(r.recvline().decode())
    print(data)
    data = data['hand'].split(' of ')
    hand = VALUES.index(data[0]) + 13 * SUITS.index(data[1])
    arr.append(hand)
print(arr)
state = []
for i in range(0, len(arr), 11):
    s = 0
    for j in range(i, i + 11):
        s += arr[j] * 52 ** (10 - (j - i))
    state.append(s)
print(state)
print(state[0].bit_length())
print(state[1].bit_length())
print(state[2].bit_length())

a = (state[1] - state[2]) * (0 - inverse(state[0] - state[1], mod)) % mod
b = (state[2] - a * state[1]) % mod

if (state[1] - b - state[0] * a) % mod != 0:
    a = (state[1] - state[2]) * inverse(state[0] - state[1], mod) % mod
    b = (state[2] - a * state[1]) % mod
assert (state[1] - b - state[0] * a) % mod == 0
# while True:
size = len(state)
state.append((a * state[size - 1] + b) % mod)
deals = rebase(state[size], 52)
current_state = state[size]
print(deals)
while True:
    try:
        hidden = deals.pop()
        if len(deals) == 0:
            current_state = (current_state * a + b) % mod
            deals = rebase(current_state, 52)
        hidden = hidden % 13
        hand = hand % 13
        if hidden == hand:
            send = {'choice': 'l'}
        elif hidden < hand:
            send = {'choice': 'l'}
        else:
            send = {'choice': 'h'}
        send = json.dumps(send).encode()
        r.sendline(send)
        data = json.loads(r.recvline().decode())
        print(data)
        hand = hidden
    except:
        r.interactive()