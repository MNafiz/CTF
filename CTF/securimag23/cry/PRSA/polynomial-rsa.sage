def get_unit_irreducible(R):
    P = R.random_element((50,75))
    while not P.is_irreducible() and not P.is_unit():
        P = R.random_element((50,75))
    return P

def iter_to_polynome(R, message):
    P = R.random_element(-1)
    for ind, chr in enumerate(message):
        P += ord(chr)*X**ind
    return P

p = Integer(input("p : "))
if not p.is_prime():
    raise ValueError("p should be a prime number")

e = Integer(input("e : "))
message = input("What do you want to cipher ?")

R.<X> = PolynomialRing(GF(p))

P = get_unit_irreducible(R)
Q = get_unit_irreducible(R)

print("Private key:")
print("p : {}".format(hex(p)))
print("e : {}".format(hex(e)))
print("Q(X) = {}".format(Q))
print("P(X) = {}".format(P))

N = P*Q

M = iter_to_polynome(R,message)

C = pow(M,e,N)

print("Public key:")
print("p : {}".format(hex(p)))
print("e : {}".format(hex(e)))
print("N(X) = {}".format(N))


print("Cipher :")
print("C(X) = {}".format(C))
