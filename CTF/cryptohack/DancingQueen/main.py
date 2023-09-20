from Crypto.Util.number import long_to_bytes


def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]


def rotate(x, n):
    return ((x << (32 - n)) & 0xffffffff) | ((x >> n) & 0xffffffff)


def word(x):
    return x % (2 ** 32)


def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])


def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])


def _quarter_round(x, a, b, c, d):
    x[b] = rotate(x[b], 7)
    x[b] ^= x[c]
    x[c] = word(x[c] - x[d])
    x[d] = rotate(x[d], 8)
    x[d] ^= x[a]
    x[a] = word(x[a] - x[b])
    x[b] = rotate(x[b], 12)
    x[b] ^= x[c]
    x[c] = word(x[c] - x[d])
    x[d] = rotate(x[d], 16)
    x[d] ^= x[a]
    x[a] = word(x[a] - x[b])


def _inner_block(state):
    _quarter_round(state, 3, 4, 9, 14)
    _quarter_round(state, 2, 7, 8, 13)
    _quarter_round(state, 1, 6, 11, 12)
    _quarter_round(state, 0, 5, 10, 15)
    _quarter_round(state, 3, 7, 11, 15)
    _quarter_round(state, 2, 6, 10, 14)
    _quarter_round(state, 1, 5, 9, 13)
    _quarter_round(state, 0, 4, 8, 12)


_counter = 1


def _setup_state(key, iv):
    _state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    _state.extend(bytes_to_words(key))
    _state.append(_counter)
    _state.extend(bytes_to_words(iv))
    return _state


msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')

state = xor(msg[0:64], msg_enc[0:64])
state = bytes_to_words(state)
print(state)
for j in range(10):
    _inner_block(state)
print(state)
key = words_to_bytes(state[4:-4])
iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
state = _setup_state(key, iv2)
print(state)


def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)


def _quarter_round(x, a, b, c, d):
    x[a] = word(x[a] + x[b])
    x[d] ^= x[a]
    x[d] = rotate(x[d], 16)
    x[c] = word(x[c] + x[d])
    x[b] ^= x[c]
    x[b] = rotate(x[b], 12)
    x[a] = word(x[a] + x[b])
    x[d] ^= x[a]
    x[d] = rotate(x[d], 8)
    x[c] = word(x[c] + x[d])
    x[b] ^= x[c]
    x[b] = rotate(x[b], 7)


def _inner_block(state):
    _quarter_round(state, 0, 4, 8, 12)
    _quarter_round(state, 1, 5, 9, 13)
    _quarter_round(state, 2, 6, 10, 14)
    _quarter_round(state, 3, 7, 11, 15)
    _quarter_round(state, 0, 5, 10, 15)
    _quarter_round(state, 1, 6, 11, 12)
    _quarter_round(state, 2, 7, 8, 13)
    _quarter_round(state, 3, 4, 9, 14)


for j in range(10):
    _inner_block(state)
print(state)
flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')
byte_state = b''
state = b''.join([i.to_bytes(4, 'little') for i in state])
print(xor(state, flag_enc))