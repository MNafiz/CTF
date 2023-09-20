from itertools import combinations

list_angka = [1,2,3,4,5]

pasangan = list(combinations(list_angka,2))

for pasang in pasangan:
    tmp = list(pasang)
    print(tmp)