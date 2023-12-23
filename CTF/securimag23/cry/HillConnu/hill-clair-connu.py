from sympy.matrices import Matrix

table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .="
encode = lambda x: table.index(x) # Caractère -> indice dans la table
decode = lambda x: table[x] # Indice dans la table -> caractère
unpad = lambda x : x.strip("=") # Enleve le potentiel padding
pad = lambda x, n: x + "=" * (n - (len(x) % n)) # Rajoute du padding si besoin

# Applique l'algorithme de chiffrement (ou déchiffrement si M est l'inverse de la clé)
def hill_apply(inp, M):

    m = [encode(char) for char in inp] # Etape 1
    n = M.cols
    l = len(m)

    assert(l % n == 0)

    c = []
    for i in range(0, l, n):
        vi = Matrix(m[i : i + n]) # Etape 2
        ci = (M * vi) % 29 # Etape 3
        c += list(ci)

    return "".join([decode(char) for char in c]) # Etape 4

def exemple():

    M = Matrix([[22, 14],[21, 23]])
    inp = pad("SECURIMAG", 2)
    out = hill_apply(inp, M)

    # Vérifie que le le déchiffrement est bien l'inverse du chiffrement
    assert(unpad(hill_apply(out,  M.inv_mod(29))) == "SECURIMAG")
    print(hill_apply("MJORWIAMBARFOIJXWSX.XIGOGRBPTOHDQWHPVZHUAKPELHYVHNAHNZHQ", M.inv_mod(29)))

if __name__ == '__main__':
    exemple()
