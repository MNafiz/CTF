from pwn import *
import math

context.log_level = "warning"
# FREQ = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,  
#  'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,  
#  'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,  
#  'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

frequ = [0.2039, 0.0264, 0.0076, 0.05, 0.0828,
         0.0021, 0.0366, 0.0274, 0.0798, 0.0087,
          0.00514, 0.00326, 0.00421, 0.0933, 0.0126,
           0.0261, 0.0001, 0.0464, 0.0415, 0.0558,
            0.0462, 0.0018, 0.0048, 0.0003, 0.0188, 0.0004 ]

FREQ = {
     chr(i+97) : frequ[i] for i in range(len(frequ))
}


def bhattacharyya_distance(dist1: dict, dist2: dict) -> float:  
    bc_coeff = 0  
    for letter in FREQ.keys():  
        bc_coeff += math.sqrt(dist1[letter] * dist2[letter])  
    return -math.log(bc_coeff)


def score_string(word: bytes) -> float:  
	curr_freq = {letter: 0 for letter in FREQ.keys()}  

	# calc letter dist for current word  
	num_letters = 0  
	for i in word:  
		if chr(i).lower() in FREQ.keys():  
			curr_freq[chr(i).lower()] += 1  
			num_letters += 1  

	if num_letters != 0:  
		curr_freq = {letter: val / num_letters for letter, val in curr_freq.items()}  
	else:  
		return 0  

	# evaluate dist using the Bhattacharyya distance  
	distance = bhattacharyya_distance(FREQ, curr_freq)  
	return 1 / distance

def decode_single_byte(src):  
    max_score = 0  
    best_res = b''  
    for i in range(2 ** 8):  
        tmp = xor(src, i)  
        score = score_string(tmp)  
    
        if score > max_score:  
            max_score = score  
            best_res = tmp
            best = i 

    return best

block_1 = []
block_2 = []

NC = "nc 103.145.226.206 13831".split()

for iterasi in range(5):
    print(iterasi+1)
    r = remote(NC[1], NC[2])
    # r = process(["python3", "cj.py"])
    r.recvuntil(b"gift: ")
    nonce, ctflag = eval(r.recvline(0))
    nonce = bytes.fromhex(nonce)
    ctflag = bytes.fromhex(ctflag)


    ctflag = [ctflag[i:i+16] for i in range(0, len(ctflag), 16)]

    payload = b"00"*32

    r.sendlineafter(b"(hex): ", payload)

    nonce1, ct1 = eval(r.recvline(0))
    ct1 = bytes.fromhex(ct1)
    nonce1 = bytes.fromhex(nonce1)

    ct1 = [ct1[i:i+16] for i in range(0, len(ct1), 16)]

    idxs = []
    for idx,(i,j) in enumerate(zip(ct1[0], ct1[1])):
        if i == j:
            # print(idx)
            idxs.append(idx)
    # print(ct1)



    r.sendlineafter(b"(hex): ", payload)

    nonce2, ct2 = eval(r.recvline(0))
    ct2 = bytes.fromhex(ct2)
    nonce2 = bytes.fromhex(nonce2)

    ct2 = [ct2[i:i+16] for i in range(0, len(ct2), 16)]

    # print(ct2)


    # print(ctflag)
    # print(idxs)

    ctflag_temp_1 = [ctflag[0][i] for i in idxs]
    ctflag_temp_2 = [ctflag[1][i] for i in idxs]


    # src = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')  




    # for i in ctflag_temp:
    # 	print(ctflag[0].index(bytes([i])))

    ctflag_tot = [ctflag_temp_1, ctflag_temp_2]

    # print(ctflag_tot)
    ctflag_tot_trans = list(map(list, zip(*ctflag_tot)))

    key = []
    for block in ctflag_tot_trans:
        key.append(decode_single_byte(bytes(block)))

    # print(key)

    pos_key = [0  for i in range(16)]

    for i,j in zip(idxs, key):
        pos_key[i] = j

    # print(pos_key)


    aaa = xor(ctflag[0], bytes(pos_key))
    aaa = list(aaa)
    for i in range(len(pos_key)):
        if pos_key[i] == 0:
                aaa[i] = 32
    aaa = bytes(aaa)

    # print(aaa)

    block_1.append(aaa)

    aaa = xor(ctflag[1], bytes(pos_key))
    aaa = list(aaa)
    for i in range(len(pos_key)):
        if pos_key[i] == 0:
                aaa[i] = 32
    aaa = bytes(aaa)

    # print(aaa)

    block_2.append(aaa)


    r.close()


print(block_1)
print(block_2)

freq_1 = [[] for i in range(16)]
freq_2 = [[] for i in range(16)]

for blocks in block_1:
     i = 0
     for block in blocks:
          freq_1[i].append(block)
          i += 1

print(freq_1)

for i in range(len(freq_1)):
     freq_1[i] = max(freq_1[i], key=freq_1[i].count)

print(freq_1)
print(bytes(freq_1))

print(ct1)
print(ct2)

# print(max(block_1[0], key=block_1[0].count))


r = remote(NC[1], NC[2])


r.interactive()

# ce539864bdc20b979f382cd557152d2dd2698d648bd8389dac333ef912786b6a
# 76ec19262cd01b13d635cbb8a5d1de116ad60c261aca2819e53ed994e0bc9856
# e5285e2346dbb91e24cc5f8fee06ce9df9124b2370c18a1417c74da3ab6b88da